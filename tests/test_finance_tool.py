from ..src.finance_tool import FileSystem

class TestFileSystem:

    def test_iterate_largest_numeric_dir_name_one_level(self, tmp_path):
        test_file_system = FileSystem(tmp_path)
        first_dir = tmp_path / "first_level" 
        first_dir.mkdir()
        for i in range(5):
            dir_file = first_dir / str(i)
            dir_file.mkdir()
        
        assert test_file_system.iterate_largest_numeric_dir_name(first_dir,1) == first_dir / "4"