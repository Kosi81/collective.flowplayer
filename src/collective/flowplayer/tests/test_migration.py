# -*- coding: utf-8 -*-
from collective.flowplayer.utils import properties_to_dict
from collective.flowplayer.utils import flash_properties_to_dict
from collective.flowplayer.testing import \
    COLLECTIVE_FLOWPLAYER_INTEGRATION_TESTING

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from collective.flowplayer.migration import migrateTo30


class TestMigration30(unittest.TestCase):

    layer = COLLECTIVE_FLOWPLAYER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.props = getToolByName(self.portal, 'portal_properties').flowplayer_properties
        # add old properties, defined in previous versions of collective.flowplayer
        self.props.manage_addProperty('autoPlay', False, 'boolean')
        self.props.manage_addProperty('autoBuffering', True, 'boolean')
        self.props.manage_addProperty('initialScale', 'fit', 'string')
        self.props.manage_addProperty('showVolumeSlider', False, 'boolean')
        self.props.manage_addProperty('controlBarGloss', False, 'boolean')
        self.props.manage_addProperty('useNativeFullScreen', True, 'boolean')

    def test_migration(self):
        # assert values defined in propertiestool.xml
        self.assertEqual(self.props.getProperty('clip/autoPlay'), False)
        self.assertEqual(self.props.getProperty('clip/autoBuffering'), False)
        self.assertEqual(self.props.getProperty('plugins/controls/volume'), True)
        self.assertEqual(self.props.getProperty('clip/scaling'), 'fit')
        migrateTo30(self.portal)
        # check values are migrated
        self.assertEqual(self.props.getProperty('clip/autoPlay'), False)
        self.assertEqual(self.props.getProperty('clip/autoBuffering'), True)
        self.assertEqual(self.props.getProperty('clip/scaling'), 'fit')
        self.assertEqual(self.props.getProperty('plugins/controls/volume'), False)
        # old properties has to be removed now
        self.failIf(self.props.hasProperty('autoPlay'))
        self.failIf(self.props.hasProperty('autoBuffering'))
        self.failIf(self.props.hasProperty('showVolumeSlider'))
        self.failIf(self.props.hasProperty('initalScale'))
        # Those are deleted because not migrated at all
        self.failIf(self.props.hasProperty('controlBarGloss'))
        self.failIf(self.props.hasProperty('useNativeFullScreen'))

