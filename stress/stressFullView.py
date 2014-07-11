#!/usr/bin/python
# coding:utf-8

from uiautomatorplug.android import device as d
import unittest
import commands
import string
import time
import sys
import util
import os

u = util.Util()

PATH = os.getcwd()

PACKAGE_NAME = 'com.intel.android.gallery3d'
ACTIVITY_NAME = PACKAGE_NAME + '/.app.Gallery'

class GalleryTest(unittest.TestCase):
    def setUp(self):
        super(GalleryTest,self).setUp()
        #Add on May 26th due to device always reboot by itself
        if d(text = 'Charged').wait.exists(timeout = 2000):
            commands.getoutput('adb root')
            time.sleep(5)
            commands.getoutput('adb remount')
            d.swipe(530,1300,1000,1300)
        u._clearAllResource()
        


    def tearDown(self):
        super(GalleryTest,self).tearDown()
        u.pressBack(4)

    def testCropPicture(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            u.setMenuOptions('Crop')
            assert d(text = 'Crop picture').wait.exists(timeout = 3000)
            d(text = 'Crop').click.wait()
            assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testCropPictureCancel(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            u.setMenuOptions('Crop')
            assert d(text = 'Crop picture').wait.exists(timeout = 3000)
            d(text = 'Cancel').click.wait()
            assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testAddEvent(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            self._addKeyWordEventVenue('event',"shangban")
            time.sleep(1)
            assert d(text = 'shangban').wait.exists(timeout =2000),'add event fail' 
            d(resourceId='com.intel.android.gallery3d:id/event_text').click.wait() 
            time.sleep(1)
            d(resourceId='com.intel.android.gallery3d:id/search_text_clear').click.wait()  
            d.click(2358,1090)     
            time.sleep(1)


    def testAddPlace(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            self._addKeyWordEventVenue('venue',"kaihui")
            time.sleep(1)
            assert d(text = 'kaihui').wait.exists(timeout =2000),'add event fail' 
            d(resourceId='com.intel.android.gallery3d:id/venue_text').click.wait() 
            time.sleep(1)
            d(resourceId='com.intel.android.gallery3d:id/search_text_clear').click.wait()  
            d.click(2358,1090)     
            time.sleep(1)

    def testTagOnePicture(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            self._addKeyWordEventVenue('Keyword',"test-%s" %i) 
            time.sleep(1)   
            assert d(text = "test-%s" %i).wait.exists(timeout =2000),'add tag fail'  

    def testSetAsContact(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(2):
            self._setPicAs('contact')
            d(index = 2).click.wait()
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            time.sleep(2)
            d(text = 'Crop').click.wait()
            assert d(description = 'Share').wait.exists(timeout = 2000)

    def testSetAsWallpaper(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(2):
            self._setPicAs('wallpaper')
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            d(text = 'Crop').click.wait()
            time.sleep(2)
            assert d(description = 'Share').wait.exists(timeout = 5000)

    def testViewPicture(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(2):
            d.press('back') #If it goes to fullview suc, it shall back to the grid view after pressing back key
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)
            u.pressBack(4)
            u.launchGallery()
            u.enterXView('fullview')

    def testUPIcon(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(2):
            d(resourceId = 'android:id/home').click.wait()
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)
            u.pressBack(4)
            u.launchGallery()
            u.enterXView('fullview')
            u.showPopCard()

    def testSlidePicture(self):
        self._clearAndPush500Pic()
        u.launchGallery()
        u.enterXView('fullview')
        d.click(550,150)
        d.click(550,150)
        time.sleep(10)
        assert d(description = 'Share').wait.exists(timeout = 5000), 'Pop card does not display after tapping on the top bar twice'       
        for i in range(2):
            for j in range(10):
                self._slideImageRtoL()
            for k in range(10):
                self._slideImageLtoR()

    def testDeleteOneByOne(self):
        self._clearAndPush500Pic()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(2):
            u.setMenuOptions('Delete')
            d(text = 'Delete').click.wait() #Confirm it

    def testPlayPauseVideo(self):
        self._clearAndPushVideo()
        u.launchGallery()
        u.enterXView('fullview')
        for i in range(100):
            u.tapOnCenter() #Press playback icon
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            time.sleep(10) #Play video file 10 s
            d.click(550,150)
            d.click(550,150) #Invoke pop card
            assert d(className = 'android.widget.ImageView').wait.exists(timeout = 2000)
            #d(resourceId = 'android:id/up').click.wait() #Back to the fullview
            u.pressBack(1)





    def _clearAndPushVideo(self):
        commands.getoutput('adb shell rm -r /mnt/sdcard/testalbum/')
        #commands.getoutput('adb push ' + os.getcwd() + '/resource/testvideo/ ' + '/sdcard/testvideo')
        commands.getoutput('adb push ' + PATH + '/script/resource/testvideo/ ' + '/sdcard/testvideo')
        #Refresh media
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def _clearAndPush500Pic(self):
        commands.getoutput('adb shell rm -r /mnt/sdcard/testalbum/')
        #commands.getoutput('adb push ' + os.getcwd() + '/resource/testStress500pic/ /sdcard/testStress500pic')
        commands.getoutput('adb push ' + PATH + '/script/resource/testStress500pic/ ' + '/sdcard/testStress500pic')
        #Refresh media
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def _setPicAs(self,setact):
        d.press('menu')
        d(text = 'Set picture as').click.wait()
        setmode = {'contact':'Contact photo', 'wallpaper':'com.intel.android.gallery3d'}
        d(text = setmode[setact]).click.wait()

    def _tapOnDoneButton(self):
        #Touch on Done button on the soft keyboard
        d.click(1100,1660)

    def _slideImageRtoL(self):
        #Swipe screen from right to left
        d.swipe(1000,1000,1,1000,2)
        time.sleep(2)

    def _slideImageLtoR(self):
        #Swipe screen from left to right
        d.swipe(1,1000,1000,1000,2)
        time.sleep(2)
    
    def _addKeyWordEventVenue(self,word,text): 
        if word == 'Keyword' :
            while not d(resourceId='com.intel.android.gallery3d:id/add'+ word + 'Button').wait.exists(timeout=3000):
                d().swipe.up()
            time.sleep(1)
            d().swipe.up()
            time.sleep(2)  
            d(resourceId='com.intel.android.gallery3d:id/add'+ word + 'Button').click.wait()
            time.sleep(1)
            d(text ="Enter new keyword").set_text(text)
            time.sleep(1)                  
        else:
            u.slideDown()
            while not d(resourceId='com.intel.android.gallery3d:id/'+ word +'_text').wait.exists(timeout=2000):
                u.slideDown()
            time.sleep(1)  
            d(resourceId='com.intel.android.gallery3d:id/'+ word +'_text').click.wait()
            time.sleep(1)
            d(text ="Enter new " + word).set_text(text)
            time.sleep(1)
        d.click(2358,1090)
