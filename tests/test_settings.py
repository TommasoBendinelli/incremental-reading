from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch


class SettingsTests(TestCase):
    def setUp(self):
        modules = {
            'anki.hooks': MagicMock(),
            'aqt': MagicMock(),
            'aqt.utils': MagicMock(),
            'ir.about': MagicMock(),
            'ir.main': MagicMock(),
            'ir.util': MagicMock(),
        }
        patch.dict('sys.modules', modules).start()
        patch('ir.settings.json.load', MagicMock()).start()
        pf_mock = MagicMock(return_value=str())
        patch('ir.settings.mw.pm.profileFolder', pf_mock).start()
        patch('ir.settings.open', mock_open()).start()
        if_mock = MagicMock(return_value=True)
        patch('ir.settings.os.path.isfile', if_mock).start()
        from ir.settings import SettingsManager
        self.sm = SettingsManager()

    def tearDown(self):
        patch.stopall()

    def test_save(self):
        open_mock = mock_open()
        dump_mock = MagicMock()
        open_patcher = patch('ir.settings.open', open_mock)
        dump_patcher = patch('ir.settings.json.dump', dump_mock)
        open_patcher.start()
        dump_patcher.start()
        self.sm.getSettingsPath = MagicMock(return_value='foo.json')
        self.sm.settings = {'foo': 'bar'}
        self.sm.save()
        open_mock.assert_called_once_with('foo.json', 'w', encoding='utf-8')
        dump_mock.assert_called_once_with({'foo': 'bar'}, open_mock())
        dump_patcher.stop()

    def test_getMediaDir(self):
        with patch('aqt.mw.pm.profileFolder', MagicMock(return_value='foo')):
            self.assertEqual(self.sm.getMediaDir(), 'foo/collection.media')

    def test_getSettingsPath(self):
        self.sm.getMediaDir = MagicMock(return_value='foo')
        self.assertEqual(self.sm.getSettingsPath(), 'foo/_ir.json')

    def test_validFormat(self):
        self.sm.requiredFormatKeys = {'test': ['foo', 'bar', 'baz']}
        self.assertTrue(self.sm.validFormat('test', '{foo}{bar}{baz}'))
        self.assertFalse(self.sm.validFormat('test', '{foo}{baz}'))
