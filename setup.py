from setuptools import setup

class BuildGRPC:
    """Generate gRPC bindings."""

    def _gen_grpc(self):
        root = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        proto_root_dir = root / 'azure' / 'durable_functions' / 'protos'
        proto_src_dir = proto_root_dir / '_src' / 'src' / 'proto'
        staging_root_dir = root / 'build' / 'protos'
        staging_dir = (staging_root_dir / 'azure'
                       / 'durable_functions' / 'protos')
        build_dir = staging_dir / 'azure' / 'durable_functions' / 'protos'

        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        shutil.copytree(proto_src_dir, build_dir)

        subprocess.run([
            sys.executable, '-m', 'grpc_tools.protoc',
            '-I', os.sep.join(('azure', 'functions_worker', 'protos')),
            '--python_out', str(staging_root_dir),
            '--grpc_python_out', str(staging_root_dir),
            os.sep.join(('azure', 'functions_worker', 'protos',
                         'azure', 'functions_worker', 'protos',
                         'FunctionRpc.proto')),
        ], check=True, stdout=sys.stdout, stderr=sys.stderr,
            cwd=staging_root_dir)

        compiled = glob.glob(str(staging_dir / '*.py'))

        if not compiled:
            print('grpc_tools.protoc produced no Python files',
                  file=sys.stderr)
            sys.exit(1)

        for f in compiled:
            shutil.copy(f, proto_root_dir)

class build(build.build, BuildGRPC):

    def run(self, *args, **kwargs):
        self._gen_grpc()
        super().run(*args, **kwargs)

setup(
    name='azure-functions-durable-python',
    version='1.0.0b10',
    description='Durable Functions Support For Python Functionapp',
    license='MIT',
    packages=['azure.durable_functions',
              'azure.durable_functions.models'],
    setup_requires=[
        'grpcio~=1.20.1',
        'grpcio-tools~=1.20.1',
    ],
    install_requires=[
        'grpcio~=1.20.1',
        'grpcio-tools~=1.20.1',
    ],
    extras_require={
        'dev': [
            'flake8==3.7.8',
            'pytest==5.0.1'
        ]
    },
    include_package_data=True,
    cmdclass={

        'build': build
    },
    test_suite='tests'
)
