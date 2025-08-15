// Copyright 2021-2025 Chair for Software & Systems Engineering, TUM
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <cstdlib>
#include <filesystem>
#include <ft/bb_info.h>
#include <ft/formatter.h>
#include <ft/io.h>
#include <llvm/ADT/ArrayRef.h>
#include <llvm/Config/llvm-config.h>
#include <llvm/IR/Analysis.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/DerivedTypes.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/PassManager.h>
#include <llvm/IR/Type.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <llvm/Support/Compiler.h>
#include <string>
#include <vector>

constexpr const char *FT_PASS_ENVVAR_OUTPUT_FILE = "FT_PASS_OUTPUT_FILE";
constexpr const char *DEFAULT_OUTPUT_FILE = "output.json";

using namespace ft;
using namespace llvm;

namespace fs = std::filesystem;

namespace {

struct FuzztasticPass : public PassInfoMixin<FuzztasticPass> {

    static auto extractProgramName(Module &M) -> std::string {
        auto programName = fs::path(M.getName().str()).filename().stem().string();

        return programName.empty() ? "unknown_program" : programName;
    }

    auto run(Module &M, ModuleAnalysisManager &) -> PreservedAnalyses {
        BBId bbId = 0;
        std::vector<BBInfo> bbInfos;

        auto &context = M.getContext();

        IRBuilder<> builder(context);
        FunctionCallee const ftIncCovFunc = M.getOrInsertFunction(
                "ft_inc_cov", FunctionType::get(Type::getVoidTy(context), {Type::getInt32Ty(context)}, false));

        auto programName = extractProgramName(M);

        for (auto &func : M) {
            if (func.isDeclaration()) {
                continue;
            }

            auto *funcProg = func.getSubprogram();
            if (funcProg == nullptr) {
                continue;
            }

            auto *progFile = funcProg->getFile();
            if (progFile == nullptr) {
                continue;
            }

            auto functionName = func.getName().str();
            auto filename = fs::path(progFile->getFilename().str()).filename().string();

            for (auto &bb : func) {
                Lines lines;

                for (auto &inst : bb) {
                    if (const auto &debugLoc = inst.getDebugLoc()) {
                        if (debugLoc.getLine() >= funcProg->getLine()) {
                            lines.insert(debugLoc.getLine());
                        }
                    }
                }

                if (!lines.empty()) {
                    // Insert a function call to the runtime library to track BB coverage, i.e., "ft_inc_cov(bbId)"
                    builder.SetInsertPoint(&bb, bb.getFirstInsertionPt());
                    builder.CreateCall(ftIncCovFunc, {ConstantInt::get(Type::getInt32Ty(context), bbId)});

                    bbInfos.emplace_back(bbId, functionName, filename, programName, lines);

                    bbId += 1;
                }
            }
        }

        const char *envOutputFile = std::getenv(FT_PASS_ENVVAR_OUTPUT_FILE);

        auto outputFile = (envOutputFile != nullptr) ? fs::absolute(fs::path(envOutputFile))
                                                     : fs::current_path() / DEFAULT_OUTPUT_FILE;

        io::writeFile(outputFile, formatter::toJSON(bbInfos));

        return PreservedAnalyses::none();
    }
};

}  // namespace

extern "C" LLVM_ATTRIBUTE_WEAK auto llvmGetPassPluginInfo() -> ::llvm::PassPluginLibraryInfo {
    return {LLVM_PLUGIN_API_VERSION, "FuzztasticPass", LLVM_VERSION_STRING, [](PassBuilder &PB) {
                PB.registerPipelineParsingCallback(
                        [](StringRef Name, ModulePassManager &MPM, ArrayRef<PassBuilder::PipelineElement>) {
                            if (Name == "fuzztastic") {
                                MPM.addPass(FuzztasticPass());
                                return true;
                            }
                            return false;
                        });
            }};
}
