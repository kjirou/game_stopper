# coding: utf-8
from django.conf import settings
import os
from django.test import TestCase
from core.utils import get_test_tmp_dir, create_test_tmp_dir, \
    delete_test_tmp_dir


class TestTmpDirManagementTest(TestCase):
    u'''テスト用一時ディレクトリ管理のテスト'''

    def test_creating_and_deleting(self):
        u'''一連の処理を確認'''
        path = get_test_tmp_dir()
        # 生成
        create_test_tmp_dir()
        # 生成確認
        self.assertTrue(os.path.isdir(path))
        # 存在時にエラーに成らないか
        create_test_tmp_dir()
        # 削除
        delete_test_tmp_dir()
        # 非存在時にエラーにならないか
        delete_test_tmp_dir()
        # 削除確認
        self.assertFalse(os.path.isdir(path))
