from datetime import datetime
from unittest import TestCase

from src.photo_sort import PhotoSort


class TestPhotoSort(TestCase):
    def test_datetime_of_underscored(self):
        actual_dt = PhotoSort.datetime_of("20210102_151344")
        self.assertEqual(datetime(year=2021, month=1, day=2, hour=15, minute=13, second=44), actual_dt)

        actual_dt = PhotoSort.datetime_of("aaa20210102_151344bbb.jpg")
        self.assertEqual(datetime(year=2021, month=1, day=2, hour=15, minute=13, second=44), actual_dt)

    def test_datetime_of_dashed(self):
        actual_dt = PhotoSort.datetime_of("2021-01-02-15-13-44")
        self.assertEqual(datetime(year=2021, month=1, day=2, hour=15, minute=13, second=44), actual_dt)

        actual_dt = PhotoSort.datetime_of("asdfasfasf2021-01-02-15-13-44asdfasfasdfa.png")
        self.assertEqual(datetime(year=2021, month=1, day=2, hour=15, minute=13, second=44), actual_dt)

    def test_datetime_of_unknown(self):
        actual_dt = PhotoSort.datetime_of("111222333")
        self.assertEqual(datetime.min, actual_dt)

        actual_dt = PhotoSort.datetime_of("")
        self.assertEqual(datetime.min, actual_dt)

    def test_datetime_of_dash_space_dot(self):
        actual_dt = PhotoSort.datetime_of("2021-01-02 15.13.44")
        self.assertEqual(datetime(year=2021, month=1, day=2, hour=15, minute=13, second=44), actual_dt)

    def test_trg_path_should_get_year_from_info(self):
        ts_of_2023 = 1689064223
        proc = PhotoSort(src_arch_dir_param="", trg_dir_param="/mytarget")
        # In file path 2021, in description 2023 year.
        actual = proc.trg_path("Photos from 1111/20210102_151344", {"photoTakenTime": {"timestamp": ts_of_2023}})
        # 2023 in description is of higher priority than 2021 in file name
        self.assertEqual("/mytarget/2023/20210102_151344", actual)

    def test_trg_path_not_album(self):
        proc = PhotoSort(src_arch_dir_param="", trg_dir_param="/mytarget")

        actual = proc.trg_path("Photos from 1111/20210102_151344")
        self.assertEqual("/mytarget/2021/20210102_151344", actual)

        actual = proc.trg_path("Photos from 1111/20210102_151344.jpg")
        self.assertEqual("/mytarget/2021/20210102_151344.jpg", actual)

        actual = proc.trg_path("Photos from 1111/aaaaa_20210102_151344_bbbbb.jpg")
        self.assertEqual("/mytarget/2021/aaaaa_20210102_151344_bbbbb.jpg", actual)

        actual = proc.trg_path("~/asdas/sdfasf/Photos from 1111/aaaaa_20210102_151344_bbbbb.jpg")
        self.assertEqual("/mytarget/2021/aaaaa_20210102_151344_bbbbb.jpg", actual)

    def test_trg_path_album(self):
        proc = PhotoSort(src_arch_dir_param="", trg_dir_param="/mytarget")

        actual = proc.trg_path("album1/20210102_151344")
        self.assertEqual("/mytarget/2021/album1/20210102_151344", actual)

        actual = proc.trg_path("2134/album1/20210102_151344.jpg")
        self.assertEqual("/mytarget/2021/album1/20210102_151344.jpg", actual)

        actual = proc.trg_path("some parent/album1/aaaaa_20210102_151344_bbbbb.jpg")
        self.assertEqual("/mytarget/2021/album1/aaaaa_20210102_151344_bbbbb.jpg", actual)

        actual = proc.trg_path("~/asdas/sdfasf/album1/aaaaa_20210102_151344_bbbbb.jpg")
        self.assertEqual("/mytarget/2021/album1/aaaaa_20210102_151344_bbbbb.jpg", actual)
