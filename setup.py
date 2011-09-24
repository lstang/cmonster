from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext

description = """
cmonster is a Python wrapper around the Clang/LLVM preprocessor, adding support
for inline Python macros, programmatic #include handling, and external
preprocessor emulation.
""".strip()

# Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
import distutils.sysconfig
cfg_vars = distutils.sysconfig.get_config_vars()
if "CFLAGS" in cfg_vars:
    cfg_vars["CFLAGS"] = cfg_vars["CFLAGS"].replace("-Wstrict-prototypes", "")

# "cmonster-core" shared library.
_cmonster_extension = Extension(
    "cmonster._cmonster",
    [
        "src/cmonster/core/impl/exception_diagnostic_client.cpp",
        "src/cmonster/core/impl/include_locator_impl.cpp",
        "src/cmonster/core/impl/function_macro.cpp",
        "src/cmonster/core/impl/parser.cpp",
        "src/cmonster/core/impl/parse_result.cpp",
        "src/cmonster/core/impl/preprocessor_impl.cpp",
        "src/cmonster/core/impl/token_iterator.cpp",
        "src/cmonster/core/impl/token_predicate.cpp",
        "src/cmonster/core/impl/token.cpp",

        "src/cmonster/python/exception.cpp",
        "src/cmonster/python/include_locator.cpp",
        "src/cmonster/python/function_macro.cpp",
        "src/cmonster/python/module.cpp",
        "src/cmonster/python/parser.cpp",
        "src/cmonster/python/parse_result.cpp",
        "src/cmonster/python/preprocessor.cpp",
        "src/cmonster/python/token.cpp",
        "src/cmonster/python/token_iterator.cpp",
        "src/cmonster/python/token_predicate.cpp"
    ],

    # Required by LLVM/Clang.
    define_macros = [("__STDC_LIMIT_MACROS", 1),
                     ("__STDC_CONSTANT_MACROS", 1)],

    # LLVM/Clang include directories.
    include_dirs = [
        "src",
        "/home/andrew/prog/llvm/tools/clang/include/",
        "/home/andrew/prog/llvm/build/tools/clang/include/",
        "/home/andrew/prog/llvm/include/",
        "/home/andrew/prog/llvm/build/include/"
    ],

    # LLVM/Clang libraries.
    #library_dirs = ["/home/andrew/prog/llvm/build/Debug+Asserts/lib"],
    library_dirs = ["/home/andrew/prog/llvm/build/Release/lib"],
    libraries = [
        "clangFrontend",
        "clangDriver",
        "clangSerialization",
        "clangParse",
        "clangSema",
        "clangAnalysis",
        "clangAST",
        "clangLex",
        "clangBasic",
        "LLVMMC",
        "LLVMSupport",
        "LLVMCore",
        "pthread",
        "dl"
    ],

    # No RTTI in Clang, so none here either.
    extra_compile_args = ["-fno-rtti"]
)

_ast_extension = Extension(
    "cmonster._ast", ["src/cmonster/python/ast/ast.pyx"],
    language = "c++",
    define_macros = _cmonster_extension.define_macros,
    include_dirs = _cmonster_extension.include_dirs,
    library_dirs = _cmonster_extension.library_dirs,
    libraries = _cmonster_extension.libraries,
    extra_compile_args = _cmonster_extension.extra_compile_args
)


classifiers = [
    "Intended Audience :: Developers",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: C",
    "Programming Language :: C++",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 3 - Alpha",
    "Topic :: Software Development :: Pre-processors"
]


setup(
    name="cmonster",
    version="0.1",
    classifiers=classifiers,
    description=description,
    packages = ["cmonster", "cmonster.config"],
    package_dir = {"": "lib"},
    scripts = ["scripts/cmonster"],
    ext_modules=[_cmonster_extension, _ast_extension],
    author="Andrew Wilkins",
    author_email="axwalk@gmail.com",
    url="http://github.com/axw/cmonster",
    test_suite="test",
    cmdclass = {"build_ext": build_ext},
)

