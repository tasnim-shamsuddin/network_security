from dataclasses import dataclass
import sys

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
    