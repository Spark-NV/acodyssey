# all credits to https://next.nexusmods.com/profile/vahndaar

import errno
import os
import sys
import winreg
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from bitstring import BitStream
from bitstring import BitArray
from bitstring import ConstBitStream
from shutil import copyfile

if platform.system().lower() == 'windows':
    from ctypes import windll, c_int, byref
    stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
    mode = c_int(0)
    windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
    mode = c_int(mode.value | 4)
    windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)
    
    windll.kernel32.FreeConsole()

NUM_TWEAKS = 28
CURRENT_VERSION = 'V1.1.2.5'
COMPATIBLE_VERSION = 'V1.5.6'

class Colors:
    GREEN = '\033[1;32;40m'
    YELLOW = '\033[1;33;40m'
    RED = '\033[1;31;40m'
    GRAY = '\033[1;30;40m'
    RESET = '\033[0m'

class cByteArrayHack:
    hackName = ''
    fileName = ''
    status = ''
    statustext = ''
    originalByteArray = ''
    modifiedByteArray = ''
    modifiedByteArray_firstpart = ''
    modifiedByteArray_secondpart = ''
    byteOffset = 0
    variableOffset = 0
    variableType = ''
    initialised = False

    def __init__(self, hackName, fileName, originalByteArray, modifiedByteArray, variableOffset, variableType):
        self.hackName = hackName
        self.fileName = fileName
        self.originalByteArray = originalByteArray
        self.variableOffset = variableOffset
        self.variableType = variableType
        if variableOffset > 0:
            temp = BitArray(modifiedByteArray)
            self.modifiedByteArray_firstpart = temp[0:variableOffset * 4]
        self.modifiedByteArray = modifiedByteArray
        self.CheckStatus()

    def CheckStatus(self):
        fileStream = ConstBitStream(filename=self.fileName)
        found = fileStream.find(self.originalByteArray, bytealigned=True)
        if len(found) > 1:
            self.status = 'ERROR!'
        elif len(found) == 1:
            self.status = 'Inactive'
            self.statustext = Colors.YELLOW + 'Inactive' + Colors.RESET
            self.byteOffset = found
        else:
            if self.variableOffset > 0:
                found = fileStream.find(self.modifiedByteArray_firstpart, bytealigned=True)
                if len(found) == 1:
                    length = len(self.modifiedByteArray) * 4
                    self.modifiedByteArray = '0x' + fileStream.read(length).hex
                    self.status = 'Active'
                    if self.variableType == 'float':
                        self.statustext = Colors.GREEN + 'Active' + Colors.RESET + ' (%.2f)' % BitArray(self.modifiedByteArray)[self.variableOffset * 4:self.variableOffset * 4 + 32].floatle
                    if self.variableType == 'byte':
                        self.statustext = Colors.GREEN + 'Active' + Colors.RESET + ' (%u)' % BitArray(self.modifiedByteArray)[self.variableOffset * 4:self.variableOffset * 4 + 8].uint
                    self.byteOffset = found
                else:
                    self.status = 'Error'
                    self.statustext = Colors.RED + 'ERROR!' + Colors.RESET
            else:
                found = fileStream.find(self.modifiedByteArray, bytealigned=True)
                if len(found) == 1:
                    self.status = 'Active'
                    self.statustext = Colors.GREEN + 'Active' + Colors.RESET
                    self.byteOffset = found
                else:
                    self.status = 'Error'
                    self.statustext = Colors.RED + 'ERROR!' + Colors.RESET

    def Enable(self):
        if self.status == 'Inactive':
            print('Enabling \'' + self.hackName + '\'...')
            fileStream = BitStream(filename=self.fileName)
            fileStream.pos = self.byteOffset[0]
            fileStream.overwrite(self.modifiedByteArray)
            print(Colors.GREEN + 'Enabling \'' + self.hackName + '\'...done!' + Colors.RESET)
            self.Save(fileStream)
            print('Checking tweak status...hang on...')
            self.CheckStatus()

    def Disable(self):
        if self.status == 'Active':
            print('Disabling \'' + self.hackName + '\'...')
            fileStream = BitStream(filename=self.fileName)
            fileStream.pos = self.byteOffset[0]
            fileStream.overwrite(self.originalByteArray)
            print(Colors.GREEN + 'Disabling \'' + self.hackName + '\'...done!' + Colors.RESET)
            self.Save(fileStream)
            print('Checking tweak status...hang on...')
            self.CheckStatus()

    def Save(self, fileStream):
        if self.status == 'Active' or self.status == 'Inactive':
            try:
                f = open(self.fileName, 'wb')
                fileStream.tofile(f)
                f.close()
                print('Updated patch written to executable: ACOdyssey.exe.')
            except IOError:
                print('Unable to write patch to file. Ensure the file isn\'t in use and try again.')
                k = input('Press a key to continue...')

def WriteMenu(tweaks, backupAvailable):
    active_tweaks = NumActiveTweaks(tweaks)
    error_tweaks = NumErrorTweaks(tweaks)
    os.system('cls')
    print('====================================================================')
    print('Fixed AC Odyssey Tweak Pack ' + CURRENT_VERSION + '(' + COMPATIBLE_VERSION + ')\tTotal:' + str(NUM_TWEAKS) + ' [' + Colors.GREEN + 'Active' + Colors.RESET + ':' + str(active_tweaks) + '] [' + Colors.RED + 'Error' + Colors.RESET + ':' + str(error_tweaks) + ']')
    print('====================================================================')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                              HORSE MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('1.  Disable Horse Speed Restriction\t\t', tweaks['horseHack'].statustext)
    print('')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                              BOAT MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('2.  Infinite Boat Row Stamina\t\t\t', tweaks['infiniteBoatRowStamina'].statustext)
    print('')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                             PLAYER MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('3.  Infinite Breath Underwater\t\t\t', tweaks['infiniteBreathUnderwater'].statustext)
    print('4.  Custom XP Multiplier\t\t\t', tweaks['customXPMultiplier'].statustext)
    print('5.  Custom Healing : Healing Factor\t\t', tweaks['customHealingReduction1'].statustext)
    print('6.  Custom Healing : Reduced Health Boosts\t', tweaks['customHealingReduction2'].statustext)
    print('')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                         PLAYER PICKUP MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('7.  Custom Resource Loot Modifier\t\t', tweaks['customResourceLootModifier2'].statustext)
    print('8.  Custom Drachmae Multiplier\t\t\t', tweaks['customDrachmaeMultiplier'].statustext)
    print('')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                            ANIMAL MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('9.  Animal Companion : Health Boost\t\t', tweaks['customTamedAnimalHealthBoost2'].statustext)
    print('10. Animal Companion : In Combat Healing\t', tweaks['customTamedAnimalInCombatHealing'].statustext)
    print('11. Animal Companion : Healing Multiplier\t', tweaks['customTamedAnimalHealingMultiplier2'].statustext)
    print('')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                             ENEMY MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('12. Custom Enemy Health Multiplier\t\t', tweaks['customEnemyHealthMultiplier'].statustext)
    print('13. Custom Enemy Damage Multiplier\t\t', tweaks['customEnemyDamageMultiplier'].statustext)
    print('14. Custom Max Enemy Level Delta\t\t', tweaks['customMaxEnemyLevelDelta'].statustext)
    print('')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('                             MISC MODS')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('15. Reduced Bounty Cooldown\t\t\t', tweaks['customReducedBountyCooldown'].statustext)
    print('16. Disable Region Levels\t\t\t', tweaks['customDisableRegionLevels1'].statustext)
    print('--------------------------------------------------------------------')
    print('R. Run Game')
    if backupAvailable:
        print('L. Restore Backup')
    else:
        print(Colors.GRAY + 'L. Restore Backup' + Colors.RESET)
    if active_tweaks > 0:
        print('D. Disable All Tweaks')
    else:
        print(Colors.GRAY + 'D. Disable All Tweaks' + Colors.RESET)
    if active_tweaks == 0:
        print('S. Create Backup')
    else:
        print(Colors.GRAY + 'S. Create Backup' + Colors.RESET)
    print('')
    print('X. Exit')
    print('====================================================================')

def is_pathname_valid(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        root_dirname, pathname = os.path.splitdrive(pathname)
        pathname = pathname[1:len(pathname)]
        root_dirname = root_dirname.rstrip(os.path.sep)
        pathname_fragment = root_dirname
        for pathname_part in pathname.split(os.path.sep):
            pathname_fragment = pathname_fragment + os.path.sep
            pathname_fragment = pathname_fragment + pathname_part
    except TypeError:
        return False
    else:
        try:
            os.lstat(pathname_fragment)
        except OSError as exc:
            if hasattr(exc, 'winerror'):
                return False
            elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                return False
            return False
        else:
            return True

def InitialiseTweaks(fileName):
    INITIALISED_TWEAKS = 1
    print('Initialising...please be patient...(%.0f%%).' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100))
    horseHack = cByteArrayHack('Disable Horse Speed Restriction', fileName, '0x7417F30F104C2440F30F104424300F2FC17606F30F114C2430498BCF', '0xEB17F30F104C2440F30F104424300F2FC17606F30F114C2430498BCF', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDrachmaeMultiplier = cByteArrayHack('Custom Drachmae Multiplier', fileName, '0xC333C0C3CC488B81880000004885C0741280B8D1000000007409F30F1080E8000000C3F30F1005CEF05F02C3CCCCCCCCCCCCCCCCCC', '0x9033C0C3CC488B81880000004885C0741B80B8D1000000007412C780E80000000000E03FF30F1080E8000000C3CCCCCCCCCCCCCCCC', 64, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDrachmaeMultiplierDisableLowerBound1 = cByteArrayHack('Custom Drachmae Multiplier - Disable Lower Bound 1', fileName, '0x7208F30F1189C4050000C3CCCCCCCCCCCCCCCCCCCCCCCCCCCC', '0x7200F30F1189C4050000C3CCCCCCCCCCCCCCCCCCCCCCCCCCCC', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDrachmaeMultiplierDisableLowerBound2 = cByteArrayHack('Custom Drachmae Multiplier - Disable Lower Bound 2', fileName, '0x76198BC70F57C0F3480F2AC0F30F59C1F3480F2CC08986B00000', '0x76008BC70F57C0F3480F2AC0F30F59C1F3480F2CC08986B00000', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDrachmaeMultiplierDisableLowerBound3 = cByteArrayHack('Custom Drachmae Multiplier - Disable Lower Bound 3', fileName, '0x0F2FB1C405000073740F28CEE80B0CCAFF488B8F00020000', '0x0F2FB1C405000074740F28CEE80B0CCAFF488B8F00020000', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDrachmaeMultiplierDisableLowerBound4 = cByteArrayHack('Custom Drachmae Multiplier - Disable Lower Bound 4', fileName, '0x0F862B02000084C00F85230200004038B70C0200000F847601000048', '0x0F842B02000084C00F85230200004038B70C0200000F847601000048', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customXPMultiplier = cByteArrayHack('Custom XP Multiplier', fileName, '0xC333C0C3CC488B81880000004885C0741280B8D1000000007409F30F1080E4000000C3F30F10057EF05F02C3CC', '0x9033C0C3CC488B81880000004885C0740980B8D1000000007400C780E40000000000C03FF30F1080E4000000C3', 64, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customXPMultiplierDisableLowerBound1 = cByteArrayHack('Custom XP Multiplier - Disable Lower Bound 1', fileName, '0x0F2F0D8DCA78017208F30F1189C0050000C3', '0x0F2F0D8DCA78017200F30F1189C0050000C3', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customXPMultiplierDisableLowerBound2 = cByteArrayHack('Custom XP Multiplier - Disable Lower Bound 2', fileName, '0x0F2F0D5AC8750176300F57C0F3480F2AC5F30F59C1F3480F2CC00F57C08987B4', '0x0F2F0D5AC8750176000F57C0F3480F2AC5F30F59C1F3480F2CC00F57C08987B4', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customXPMultiplierDisableLowerBound3 = cByteArrayHack('Custom XP Multiplier - Disable Lower Bound 3', fileName, '0x0F2FB1C005000073740F28CEE8000FCAFF488B8F00020000', '0x0F2FB1C005000074740F28CEE8000FCAFF488B8F00020000', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customXPMultiplierDisableLowerBound4 = cByteArrayHack('Custom XP Multiplier - Disable Lower Bound 4', fileName, '0x0F86FF01000084C00F85F70100004038B70B0200000F844A01000048', '0x0F84FF01000084C00F85F70100004038B70B0200000F844A01000048', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customEnemyHealthMultiplier = cByteArrayHack('Custom Enemy Health Multiplier', fileName, '0x74124883C208483BD175EEF30F1005F77A9D01C34885C074F2F30F104010C3CCCCCCCCCCCCCC', '0x74124883C208483BD175EEF30F1005F77A9D01C34885C074F2C740100000C03FF30F104010C3', 56, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customEnemyDamageMultiplier = cByteArrayHack('Custom Enemy Damage Multiplier', fileName, '0x74124883C208483BD175EEF30F1005477B9D01C34885C074F2F30F10400CC3CCCCCCCCCCCCCC', '0x74124883C208483BD175EEF30F1005477B9D01C34885C074F2C7400C0000C03FF30F10400CC3', 56, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customMaxEnemyLevelDelta = cByteArrayHack('Custom Max Enemy Level Delta', fileName, '0x4883EC28E8372100004885C074088B40184883C428C3B8040000004883C428C3', '0x4883EC28E8372100004885C07400B8FF0000004883C428C3CCCCCCCCCCCCCCCC', 30, 'byte')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customHealingReduction1 = cByteArrayHack('Custom Healing - Healing Factor', fileName, '0x488B4F18428D149D00000000F3440F2C040A440FAF453841F7E841B801000000C1FA058BC2C1E81F03D0440F45C2418BC8', '0x4C8B1DCE736903909090909090904831C9418B8BB00300004D31C0498BD1C1FA0A85C97605D1E283C201488BCA90909090', 64, 'byte')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customHealingReduction2 = cByteArrayHack('Custom Healing - Reduced Health Boosts', fileName, '0x8D1431488BCFE88A9D13003BF30F94C084C074304084ED752BE8E7DCAD00488BD84885C0741E488D4C2420E8350F95FE488D8B200600004533C0488D542420E8914860FF488B9C247002000033C0488B8C24300200004833CCE8E774BC014881C4400200005F5E5DC3CCCCCCCCCCCCCCCCCCCCCCCC', '0xEB6790488BCFE88A9D13003BF30F94C084C074304084ED752BE8E7DCAD00488BD84885C0741E488D4C2420E8350F95FE488D8B200600004533C0488D542420E8914860FF488B9C247002000033C0488B8C24300200004833CCE8E774BC014881C4400200005F5E5DC3C1FE018D1431EB92CCCCCCCC', 214, 'byte')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customResourceLootModifier1 = cByteArrayHack('Custom Resource Loot Modifier Patch 1', fileName, '0xFF50700F57C9B801000000F3480F2ACBF30F59C1F3480F2CC885C90F45C1', '0xFF50700F57C9B801000000F3480F2ACBF30F59C1E953CF160085C90F45C1', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customResourceLootModifier2 = cByteArrayHack('Custom Resource Loot Modifier Patch 2', fileName, '0x488B5C24304883C4205FC3CCCCCCCCE93B49F30DCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC', '0x488B5C24304883C4205FC3CCCCCCCCE93B49F30DCCCCCCB80000C03F660F6ED0F30F59C2F3480F2CC8B801000000E99130E9FF', 48, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customTamedAnimalHealthBoost1 = cByteArrayHack('Tamed Animal Health Boost Patch 1', fileName, '0x488BCB0F5BC0F30F5980F8010000F3440F2CC0', '0x488BCB0F5BC0F30F5980F8010000E9B9452100', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customTamedAnimalHealthBoost2 = cByteArrayHack('Tamed Animal Health Boost Patch 2', fileName, '0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC48895C240848896C24104889742418574883EC20488B4228', '0x448B90F4010000C780F40100000000C03FF30F5980F4010000448990F4010000F3440F2CC0E91DBADEFFCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC48895C240848896C24104889742418574883EC20488B4228', 26, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customTamedAnimalInCombatHealing = cByteArrayHack('Tamed Animal In Combat Healing', fileName, '0x837E3802660F6EF00F5BF60F84B0000000', '0x837E3802660F6EF00F5BF6740490909090', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customTamedAnimalHealingMultiplier1 = cByteArrayHack('Tamed Animal Healing Multiplier Patch 1', fileName, '0xF30F59059F89C001F30F5886580100000F28C8F30F118658010000', '0xE91B73610E909090F30F5886580100000F28C8F30F118658010000', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customTamedAnimalHealingMultiplier2 = cByteArrayHack('Tamed Animal Healing Multiplier Patch 2', fileName, '0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC4883EC28488B094885C9742B448B41F848895C2420488D59F84C8D0D909DFFFFBA10000000', '0xF30F59057F165FF341BB0000803E66450F6EDBF3410F59C341BB0000803F66450F6EDBF3410F58C3E9BB8C9EF1CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC4883EC28488B094885C9742B448B41F848895C2420488D59F84C8D0D909DFFFFBA10000000', 20, 'float')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customReducedBountyCooldown = cByteArrayHack('Reduced Bounty Cooldown', fileName, '0xF30F114B600F2F055003BC01F30F11432C730BC7432C00000000C6434C01488BCBE8420C0500488BCB4883C4205BE9753B0900CCCCCCCCCC', '0xF3410F58C9F30F114B600F2F054B03BC01F30F11432C730BC7432C00000000C6434C01488BCBE83D0C0500488BCB4883C4205BE9703B0900', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDisableRegionLevels1 = cByteArrayHack('Disable Region Levels Patch 1', fileName, '0x8BC803C63BD876112BD9B80100000083FB010F46D88BFBEB', '0x8BC803C63BD890902BD9B80100000083FB010F46D88BFBEB', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    customDisableRegionLevels2 = cByteArrayHack('Disable Region Levels Patch 2', fileName, '0x8D0C383BD9760E2BD8413BDD410F46DD41891EEB', '0x8D0C383BD990902BD8413BDD410F46DD41891EEB', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    infiniteBoatRowStamina = cByteArrayHack('Infinite Boat Row Stamina', fileName, '0x450F2EC8F3440F1143507407', '0x450F2EC8E959A8D1FD907407', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    infiniteBoatRowStamina2 = cByteArrayHack('Infinite Boat Row Stamina Patch 2', fileName, '0xCCCCE94B61680BCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC', '0xCCCCE94B61680BCCCC9C837B48040F85110000004157448B7B3C44897B5066450F6EC7415F9DF3440F114350E980572E02', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    infiniteBreathUnderwater = cByteArrayHack('Infinite Breath Underwater', fileName, '0xF30F1189F0050000488B4338488B100F2F82F0050000', '0xE9B8E2DBFC0F1F00488B4338488B100F2F82F0050000', 0, 'bool')
    INITIALISED_TWEAKS += 1
    print('\rInitialising...please be patient...(%.0f%%)' % float(INITIALISED_TWEAKS / NUM_TWEAKS * 100), end='', flush=True)
    infiniteBreathUnderwater2 = cByteArrayHack('Infinite Breath Underwater Patch 2', fileName, '0xCCCCE99B206207CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC', '0xCCCCE99B206207CCCCF30F1089EC050000F30F1189F0050000E9361D2403', 0, 'bool')
    print()
    tweak_collection = {'horseHack': horseHack, 'customDrachmaeMultiplier': customDrachmaeMultiplier, 'customDrachmaeMultiplierDisableLowerBound1': customDrachmaeMultiplierDisableLowerBound1, 'customDrachmaeMultiplierDisableLowerBound2': customDrachmaeMultiplierDisableLowerBound2, 'customDrachmaeMultiplierDisableLowerBound3': customDrachmaeMultiplierDisableLowerBound3, 'customDrachmaeMultiplierDisableLowerBound4': customDrachmaeMultiplierDisableLowerBound4, 'customXPMultiplier': customXPMultiplier, 'customXPMultiplierDisableLowerBound1': customXPMultiplierDisableLowerBound1, 'customXPMultiplierDisableLowerBound2': customXPMultiplierDisableLowerBound2, 'customXPMultiplierDisableLowerBound3': customXPMultiplierDisableLowerBound3, 'customXPMultiplierDisableLowerBound4': customXPMultiplierDisableLowerBound4, 'customEnemyHealthMultiplier': customEnemyHealthMultiplier, 'customEnemyDamageMultiplier': customEnemyDamageMultiplier, 'customMaxEnemyLevelDelta': customMaxEnemyLevelDelta, 'customHealingReduction1': customHealingReduction1, 'customHealingReduction2': customHealingReduction2, 'customResourceLootModifier1': customResourceLootModifier1, 'customResourceLootModifier2': customResourceLootModifier2, 'customTamedAnimalHealthBoost1': customTamedAnimalHealthBoost1, 'customTamedAnimalHealthBoost2': customTamedAnimalHealthBoost2, 'customTamedAnimalInCombatHealing': customTamedAnimalInCombatHealing, 'customTamedAnimalHealingMultiplier1': customTamedAnimalHealingMultiplier1, 'customTamedAnimalHealingMultiplier2': customTamedAnimalHealingMultiplier2, 'customReducedBountyCooldown': customReducedBountyCooldown, 'customDisableRegionLevels1': customDisableRegionLevels1, 'customDisableRegionLevels2': customDisableRegionLevels2, 'infiniteBoatRowStamina': infiniteBoatRowStamina, 'infiniteBoatRowStamina2': infiniteBoatRowStamina2, 'infiniteBreathUnderwater': infiniteBreathUnderwater, 'infiniteBreathUnderwater2': infiniteBreathUnderwater2}
    return tweak_collection

def NumActiveTweaks(tweak_list):
    active_tweaks = 0
    for item_name in tweak_list:
        item_instance = tweak_list.get(item_name)
        if isinstance(item_instance, cByteArrayHack) and item_instance.status == 'Active':
            active_tweaks += 1
    return active_tweaks

def NumErrorTweaks(tweak_list):
    error_tweaks = 0
    for item_name in tweak_list:
        item_instance = tweak_list.get(item_name)
        if isinstance(item_instance, cByteArrayHack) and item_instance.status == 'Error':
            error_tweaks += 1
    return error_tweaks

def DisplayWelcomeMessage():
    os.system('cls')
    print(' ' + Colors.GREEN + 'Welcome to AC Odyssey Tweak Pack ' + CURRENT_VERSION + '!' + Colors.RESET)
    print('By Vahndaar')
    print(' ' + Colors.YELLOW + 'Compatible With ' + COMPATIBLE_VERSION + Colors.RESET)
    print(' ' + Colors.RED + '***DISCLAIMER! MODIFY THE GAME FILES AT YOUR OWN RISK*** ' + Colors.RESET)
    print('===============================================================================================================')

def GetSteamInstallPath():
    """Find Steam installation path from Windows registry"""
    
    # Try 64-bit registry first
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Valve\Steam')
        steam_path, _ = winreg.QueryValueEx(key, 'InstallPath')
        winreg.CloseKey(key)
        return steam_path
    except WindowsError:
        pass
    
    # Try 32-bit registry
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Valve\Steam')
        steam_path, _ = winreg.QueryValueEx(key, 'InstallPath')
        winreg.CloseKey(key)
        return steam_path
    except WindowsError:
        pass
    
    # Fallback to default locations
    default_paths = [
        r'C:\Program Files (x86)\Steam',
        r'C:\Program Files\Steam'
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            return path
    
    print('Steam installation not found')
    return None

def GetSteamLibraryFolders(steam_path):
    """Get all Steam library folders from libraryfolders.vdf"""
    library_folders = []
    
    if not steam_path:
        return library_folders
    
    main_library = os.path.join(steam_path, 'steamapps')
    if os.path.exists(main_library):
        library_folders.append(main_library)
    
    libraryfolders_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
    if os.path.exists(libraryfolders_path):
        try:
            with open(libraryfolders_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                for line in lines:
                    if '"path"' in line and '\\\\' in line:
                        path_start = line.find('"path"') + 7
                        path_end = line.find('"', path_start)
                        if path_end > path_start:
                            library_path = line[path_start:path_end].replace('\\\\', '\\')
                            steamapps_path = os.path.join(library_path, 'steamapps')
                            if os.path.exists(steamapps_path):
                                library_folders.append(steamapps_path)
        except Exception as e:
            print(f'Error reading libraryfolders.vdf: {e}')
    
    return library_folders

def FindGameInSteamLibraries(library_folders):
    """Search for AC Odyssey in Steam libraries"""
    
    ac_odyssey_app_id = '812140'
    
    for library in library_folders:
        manifest_path = os.path.join(library, f'appmanifest_{ac_odyssey_app_id}.acf')
        if os.path.exists(manifest_path):
            
            possible_game_dirs = [
                'Assassin\'s Creed Odyssey',
                'Assassins Creed Odyssey',
                'Assassins Creed Odyssey',
                'AC Odyssey'
            ]
            
            for game_dir_name in possible_game_dirs:
                game_dir = os.path.join(library, 'common', game_dir_name)
                exe_path = os.path.join(game_dir, 'ACOdyssey.exe')
                
                if os.path.exists(exe_path):
                    return exe_path
            
            common_dir = os.path.join(library, 'common')
            if os.path.exists(common_dir):
                for item in os.listdir(common_dir):
                    item_path = os.path.join(common_dir, item)
                    if os.path.isdir(item_path) and 'odyssey' in item.lower():
                        exe_path = os.path.join(item_path, 'ACOdyssey.exe')
                        if os.path.exists(exe_path):
                            return exe_path
    
    print('AC Odyssey not found in Steam libraries')
    return None

def GetExeFile():
    print('Searching for game executable...via registry...', end='')
    fileName = ''
    
    keys = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache')
    try:
        i = 0
        while True:
            key_name, key_value, key_type = winreg.EnumValue(keys, i)
            if key_name.find('\\Assassin\'s Creed Odyssey\\ACOdyssey.exe.FriendlyAppName', 0) > 0:
                fileName = key_name[0:len(key_name) - 16]
            i += 1
    except WindowsError:
        print('done!')
        pass
    
    if fileName != '':
        print('ACOdyssey.exe found via registry: ' + fileName)
    else:
        print('Couldn\'t find ACOdyssey.exe via registry.')
        
        print('Searching for game executable installed via steam...')
        steam_path = GetSteamInstallPath()
        if steam_path:
            library_folders = GetSteamLibraryFolders(steam_path)
            if library_folders:
                steam_exe = FindGameInSteamLibraries(library_folders)
                if steam_exe:
                    fileName = steam_exe
                    print(Colors.GREEN + 'ACOdyssey.exe found via Steam: ' + fileName + Colors.RESET)
    
    if fileName != '':
        print('')
        keyed_input = ''
        while keyed_input != 'y' and keyed_input != 'Y' and keyed_input != 'n' and keyed_input != 'N':
            keyed_input = input('Is this the correct file path?(Y/N): ')
            if keyed_input == 'y' or keyed_input == 'Y':
                break
            if keyed_input == 'n' or keyed_input == 'N':
                fileName = ''
                break
            print('Please respond either Y or N')
    else:
        print('Couldn\'t find ACOdyssey.exe.')
    
    if fileName == '':
        fileName = input('Please enter the file path for your ACOdyssey.exe file: ')
    
    if os.path.isdir(fileName):
        potential_exe = os.path.join(fileName, 'ACOdyssey.exe')
        if os.path.isfile(potential_exe):
            print(Colors.GREEN + f'Found ACOdyssey.exe in directory: {potential_exe}' + Colors.RESET)
            fileName = potential_exe
        else:
            print('ACOdyssey.exe not found in the specified directory.')
            fileName = input('Please enter the exact path to ACOdyssey.exe: ')
    
    print('Checking file...')
    if is_pathname_valid(fileName) == False:
        print('Path is not valid, exiting...')
        raise SystemExit('Path is not valid, exiting...')
    print('Path is valid.')
    
    if not os.path.isfile(fileName):
        print('File does not exist, exiting...')
        raise SystemExit('File does not exist, exiting...')
    
    if os.path.basename(fileName).lower() != 'acodyssey.exe':
        print('Warning: File is not named ACOdyssey.exe')
        keyed_input = ''
        while keyed_input != 'y' and keyed_input != 'Y' and keyed_input != 'n' and keyed_input != 'N':
            keyed_input = input('Continue anyway? (Y/N): ')
            if keyed_input == 'y' or keyed_input == 'Y':
                break
            if keyed_input == 'n' or keyed_input == 'N':
                raise SystemExit('Exiting...')
            print('Please respond either Y or N')
    
    print('Filename is valid.')
    return fileName

def CheckForBackup(fileName: str):
    backup_dir = os.path.dirname(os.path.abspath(fileName))
    backup_file = backup_dir + os.path.sep + 'ACOdyssey.exe.backup'
    if not is_pathname_valid(backup_file):
        return False
    return True

def SaveBackup(active_tweaks: int, fileName: str):
    file_saved = False
    if active_tweaks == 0:
        keyed_input = ''
        while keyed_input != 'y' and keyed_input != 'Y' and keyed_input != 'n' and keyed_input != 'N':
            keyed_input = input('Currently no tweaks are active, would you like to backup your file? (Y/N): ')
            if keyed_input == 'y' or keyed_input == 'Y':
                backup_dir = os.path.dirname(os.path.abspath(fileName))
                backup_file = backup_dir + os.path.sep + 'ACOdyssey.exe.backup'
                copyfile(fileName, backup_file)
                break
            elif keyed_input == 'n' or keyed_input == 'N':
                break
            print('Please respond either Y or N')
    else:
        print('There are tweaks active. Disable them before saving to ensure a clean backup.')
        keyed_input = input('Press a key to continue...')
    file_saved = CheckForBackup(fileName)
    return file_saved

class ACOdysseyTweakPackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"AC Odyssey Tweak Pack {CURRENT_VERSION} ({COMPATIBLE_VERSION})")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.resizable(True, True)
        
        self.setup_styles()
        
        self.fileName = ""
        self.tweaks = {}
        self.backup_exists = False
        
        self.status_vars = {}
        self.tweak_buttons = {}
        self.tweak_info = {}
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.setup_ui()
        self.initialize_application()
    
    def setup_styles(self):
        """Configure custom styles for larger buttons"""
        style = ttk.Style()
        
        style.configure('Large.TButton', 
                       padding=(15, 8),
                       font=('Arial', 11))
        
        style.configure('Help.TButton',
                       padding=(8, 8),
                       font=('Arial', 11))
    
    def setup_ui(self):
        title_label = tk.Label(self.main_frame, text=f"Vahndaar's AC Odyssey Tweak Pack {CURRENT_VERSION}", 
                              font=("Arial", 16, "bold"), fg="blue", cursor="hand2")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        title_label.bind("<Button-1>", self.open_nexus_page)
        title_label.bind("<Enter>", lambda e: title_label.config(fg="purple"))
        title_label.bind("<Leave>", lambda e: title_label.config(fg="blue"))
        
        subtitle_label = ttk.Label(self.main_frame, text=f"Compatible with Assassin's Creed Odyssey {COMPATIBLE_VERSION}", 
                                   font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))
        
        self.file_label = ttk.Label(self.main_frame, text="Searching for ACOdyssey.exe...", foreground="blue", font=("Arial", 9))
        self.file_label.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        self.status_label = ttk.Label(self.main_frame, text=f"Available Tweaks ({NUM_TWEAKS})", font=("Arial", 14, "bold"))
        self.status_label.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        left_panel = ttk.Frame(self.main_frame, relief="flat", borderwidth=0)
        left_panel.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(0, 5))
        
        self.canvas = tk.Canvas(left_panel, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        left_panel.rowconfigure(0, weight=1)
        left_panel.columnconfigure(0, weight=1)
        
        right_panel = ttk.Frame(self.main_frame)
        right_panel.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(5, 0))
        
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)
        
        self.active_title = ttk.Label(right_panel, text="Active Tweaks (0)", font=("Arial", 14, "bold"))
        self.active_title.grid(row=0, column=0, pady=(0, 10))
        
        self.active_tweaks_frame = ttk.Frame(right_panel)
        self.active_tweaks_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.main_frame.rowconfigure(4, weight=1)
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=2)
        
        self.create_horse_section()
        self.create_boat_section()
        self.create_player_section()
        self.create_pickup_section()
        self.create_animal_section()
        self.create_enemy_section()
        self.create_misc_section()
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Run Game", style='Large.TButton', command=self.run_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create Backup", style='Large.TButton', command=self.create_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Restore Backup", style='Large.TButton', command=self.restore_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Disable All", style='Large.TButton', command=self.disable_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh Status", style='Large.TButton', command=self.refresh_status).pack(side=tk.LEFT, padx=5)
    
    def create_horse_section(self):
        self.create_collapsible_section("Horse Mods", [
            ("horseHack", "Disable Horse Speed Restriction", "bool")
        ])
    
    def create_boat_section(self):
        self.create_collapsible_section("Boat Mods", [
            ("infiniteBoatRowStamina", "Infinite Boat Row Stamina", "bool")
        ])
    
    def create_player_section(self):
        self.create_collapsible_section("Player Mods", [
            ("infiniteBreathUnderwater", "Infinite Breath Underwater", "bool"),
            ("customXPMultiplier", "Custom XP Multiplier", "float"),
            ("customHealingReduction1", "Custom Healing Factor", "int", 1, 15),
            ("customHealingReduction2", "Custom Health Boosts", "int", 1, 5)
        ])
    
    def create_pickup_section(self):
        self.create_collapsible_section("Player Pickup Mods", [
            ("customResourceLootModifier2", "Custom Resource Loot Modifier", "float", 1.0),
            ("customDrachmaeMultiplier", "Custom Drachmae Multiplier", "float")
        ])
    
    def create_animal_section(self):
        self.create_collapsible_section("Animal Mods", [
            ("customTamedAnimalHealthBoost2", "Animal Companion Health Boost", "float", 1.0),
            ("customTamedAnimalInCombatHealing", "Animal In Combat Healing", "bool"),
            ("customTamedAnimalHealingMultiplier2", "Animal Healing Multiplier", "float")
        ])
    
    def create_enemy_section(self):
        self.create_collapsible_section("Enemy Mods", [
            ("customEnemyHealthMultiplier", "Custom Enemy Health Multiplier", "float"),
            ("customEnemyDamageMultiplier", "Custom Enemy Damage Multiplier", "float"),
            ("customMaxEnemyLevelDelta", "Custom Max Enemy Level Delta", "int", 0, 255)
        ])
    
    def create_misc_section(self):
        self.create_collapsible_section("Misc Mods", [
            ("customReducedBountyCooldown", "Reduced Bounty Cooldown", "bool"),
            ("customDisableRegionLevels1", "Disable Region Levels", "bool")
        ])
    
    def create_collapsible_section(self, title, tweaks_list):
        section_frame = ttk.Frame(self.scrollable_frame)
        section_frame.pack(fill=tk.X, padx=10, pady=5)
        
        header_frame = ttk.Frame(section_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        title_label = ttk.Label(header_frame, text=f"━━ {title} ━━", font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT)
        
        toggle_btn = ttk.Button(header_frame, text="▼", width=5, style='Help.TButton',
                               command=lambda: self.toggle_section(content_frame, toggle_btn))
        toggle_btn.pack(side=tk.RIGHT)
        
        content_frame = ttk.Frame(section_frame)
        content_frame.pack(fill=tk.X, padx=20)
        
        for i, tweak_info in enumerate(tweaks_list):
            tweak_name = tweak_info[0]
            display_name = tweak_info[1]
            value_type = tweak_info[2]
            
            min_val = None
            max_val = None
            if len(tweak_info) > 3:
                if value_type == "float":
                    min_val = tweak_info[3]
                elif value_type == "int":
                    min_val = tweak_info[3]
                    if len(tweak_info) > 4:
                        max_val = tweak_info[4]
            
            self.create_tweak_widget(content_frame, tweak_name, display_name, i, value_type, min_val, max_val)
    
    def toggle_section(self, content_frame, toggle_btn):
        if content_frame.winfo_viewable():
            content_frame.pack_forget()
            toggle_btn.config(text="▶")
        else:
            content_frame.pack(fill=tk.X, padx=20)
            toggle_btn.config(text="▼")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_tweak_widget(self, parent, tweak_name, display_name, row, value_type="bool", min_val=None, max_val=None):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5, padx=10)
        frame.columnconfigure(1, weight=1)
        
        name_label = ttk.Label(frame, text=display_name, font=("Arial", 13, "bold"))
        name_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        status_frame = ttk.Frame(frame)
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        status_label = ttk.Label(status_frame, text="Status:", font=("Arial", 12))
        status_label.pack(side=tk.LEFT)
        
        self.status_vars[tweak_name] = tk.StringVar(value="Unknown")
        status_value = ttk.Label(status_frame, textvariable=self.status_vars[tweak_name], font=("Arial", 12))
        status_value.pack(side=tk.LEFT, padx=(5, 0))
        
        if not hasattr(self, 'status_labels'):
            self.status_labels = {}
        self.status_labels[tweak_name] = status_value
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        enable_btn = ttk.Button(button_frame, text="Enable", style='Large.TButton',
                               command=lambda name=tweak_name: self.enable_tweak(name))
        enable_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        disable_btn = ttk.Button(button_frame, text="Disable", style='Large.TButton',
                                command=lambda name=tweak_name: self.disable_tweak(name))
        disable_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        help_btn = ttk.Button(button_frame, text="?", style='Help.TButton', width=5,
                             command=lambda name=tweak_name: self.show_help(name))
        help_btn.pack(side=tk.LEFT)
        
        self.tweak_buttons[tweak_name] = {"enable": enable_btn, "disable": disable_btn}
        self.tweak_info[tweak_name] = {"type": value_type, "min": min_val, "max": max_val}
    
    def initialize_application(self):
        self.find_game_file()
        
        if self.fileName:
            self.check_and_initialize_tweaks()
        else:
            self.status_label.config(text="Please select ACOdyssey.exe file")
    
    def check_and_initialize_tweaks(self):
        """Check if file is set and initialize tweaks if needed"""
        if self.fileName and not self.tweaks:
            self.initialize_tweaks()
    
    def find_game_file(self):
        try:
            keys = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache')
            i = 0
            while True:
                key_name, key_value, key_type = winreg.EnumValue(keys, i)
                if key_name.find('\\Assassin\'s Creed Odyssey\\ACOdyssey.exe.FriendlyAppName', 0) > 0:
                    self.fileName = key_name[0:len(key_name) - 16]
                    break
                i += 1
        except WindowsError:
            pass
        
        if not self.fileName:
            steam_path = GetSteamInstallPath()
            if steam_path:
                library_folders = GetSteamLibraryFolders(steam_path)
                if library_folders:
                    steam_exe = FindGameInSteamLibraries(library_folders)
                    if steam_exe:
                        self.fileName = steam_exe
        
        if self.fileName:
            self.file_label.config(text=self.fileName, foreground="green")
            self.backup_exists = CheckForBackup(self.fileName)
        else:
            self.file_label.config(text="ACOdyssey.exe not found automatically", foreground="orange")
            self.prompt_for_file()
    
    def prompt_for_file(self):
        """Prompt user to browse for ACOdyssey.exe file"""
        result = messagebox.askyesno("File Not Found", 
                                   "ACOdyssey.exe was not found automatically.\n\n"
                                   "Would you like to browse for the file manually?")
        if result:
            self.browse_file()
        else:
            self.file_label.config(text="Please select ACOdyssey.exe to continue", foreground="red")
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select ACOdyssey.exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            if os.path.basename(filename).lower() == 'acodyssey.exe':
                self.fileName = filename
                self.file_label.config(text=self.fileName, foreground="green")
                self.backup_exists = CheckForBackup(self.fileName)
                self.check_and_initialize_tweaks()
            else:
                messagebox.showerror("Error", "Please select ACOdyssey.exe file")
    
    def initialize_tweaks(self):
        if not self.fileName:
            return
        
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Initializing...")
        loading_window.geometry("400x150")
        loading_window.resizable(False, False)
        loading_window.transient(self.root)
        loading_window.grab_set()
        
        loading_window.update_idletasks()
        x = (loading_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (loading_window.winfo_screenheight() // 2) - (150 // 2)
        loading_window.geometry(f"400x150+{x}+{y}")
        
        loading_frame = ttk.Frame(loading_window, padding="20")
        loading_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(loading_frame, text="Initializing AC Odyssey Tweak Pack", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        status_var = tk.StringVar(value="Initializing...please be patient...")
        status_label = ttk.Label(loading_frame, textvariable=status_var)
        status_label.pack(pady=(0, 10))
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(loading_frame, variable=progress_var, 
                                      maximum=NUM_TWEAKS, length=300)
        progress_bar.pack(pady=(0, 10))
        
        percent_var = tk.StringVar(value="0%")
        percent_label = ttk.Label(loading_frame, textvariable=percent_var)
        percent_label.pack()
        
        loading_window.update()
        
        try:
            self.tweaks = self.initialize_tweaks_with_progress(loading_window, status_var, progress_var, percent_var)
            self.update_all_status()
            self.status_label.config(text=f"Available Tweaks ({NUM_TWEAKS})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize tweaks: {str(e)}")
            self.status_label.config(text="Initialization failed")
        finally:
            loading_window.destroy()
    
    def initialize_tweaks_with_progress(self, loading_window, status_var, progress_var, percent_var):
        tweaks = {}
        INITIALISED_TWEAKS = 0
        
        def update_progress(*args, **kwargs):
            nonlocal INITIALISED_TWEAKS
            message = ' '.join(str(arg) for arg in args)
            if "Initialising...please be patient" in message:
                INITIALISED_TWEAKS += 1
                progress_var.set(INITIALISED_TWEAKS)
                percent = int((INITIALISED_TWEAKS / NUM_TWEAKS) * 100)
                percent_var.set(f"{percent}%")
                status_var.set(f"Initializing tweak {INITIALISED_TWEAKS} of {NUM_TWEAKS}...")
                loading_window.update()
        
        original_print = print
        
        try:
            import builtins
            builtins.print = update_progress
            
            tweaks = InitialiseTweaks(self.fileName)
            
        finally:
            builtins.print = original_print
        
        return tweaks
    
    def update_all_status(self):
        for tweak_name, status_var in self.status_vars.items():
            if tweak_name in self.tweaks:
                tweak = self.tweaks[tweak_name]
                if tweak.status == 'Active':
                    status_var.set("Active")
                    self.update_button_states(tweak_name, True)
                elif tweak.status == 'Inactive':
                    status_var.set("Inactive")
                    self.update_button_states(tweak_name, False)
                else:
                    status_var.set("Error")
                    self.update_button_states(tweak_name, False)
        
        self.update_active_tweaks_display()
        self.update_status_colors()
    
    def update_status_colors(self):
        """Update the colors of status labels based on their values"""
        for tweak_name, status_var in self.status_vars.items():
            if tweak_name in self.status_labels:
                status_text = status_var.get()
                if status_text == "Active":
                    self.status_labels[tweak_name].configure(foreground="green")
                elif status_text == "Inactive":
                    self.status_labels[tweak_name].configure(foreground="red")
                elif status_text == "Error":
                    self.status_labels[tweak_name].configure(foreground="orange")
                else:
                    self.status_labels[tweak_name].configure(foreground="black")
    
    def update_button_states(self, tweak_name, is_active):
        """Update button states based on tweak status"""
        if tweak_name not in self.tweak_buttons:
            return
        
        enable_btn = self.tweak_buttons[tweak_name]["enable"]
        disable_btn = self.tweak_buttons[tweak_name]["disable"]
        tweak_info = self.tweak_info.get(tweak_name, {})
        
        if is_active:
            if tweak_info.get("type") in ["float", "int"]:
                enable_btn.config(text="Change Value", state="normal", style='Large.TButton')
                enable_btn.config(command=lambda name=tweak_name: self.change_tweak_value(name))
            else:
                enable_btn.config(text="Enable", state="disabled", style='Large.TButton')
            disable_btn.config(state="normal")
        else:
            enable_btn.config(text="Enable", state="normal", style='Large.TButton')
            enable_btn.config(command=lambda name=tweak_name: self.enable_tweak(name))
            disable_btn.config(state="disabled")
    
    def update_active_tweaks_display(self):
        for widget in self.active_tweaks_frame.winfo_children():
            widget.destroy()
        
        active_tweaks = []
        
        for tweak_name, tweak in self.tweaks.items():
            if isinstance(tweak, cByteArrayHack) and tweak.status == 'Active':
                if tweak_name in ["infiniteBoatRowStamina2", "infiniteBreathUnderwater2", 
                                "customDisableRegionLevels2", "customResourceLootModifier1",
                                "customTamedAnimalHealthBoost1", "customTamedAnimalHealingMultiplier1",
                                "customXPMultiplierDisableLowerBound1", "customXPMultiplierDisableLowerBound2",
                                "customXPMultiplierDisableLowerBound3", "customXPMultiplierDisableLowerBound4",
                                "customDrachmaeMultiplierDisableLowerBound1", "customDrachmaeMultiplierDisableLowerBound2",
                                "customDrachmaeMultiplierDisableLowerBound3", "customDrachmaeMultiplierDisableLowerBound4"]:
                    continue
                
                display_name = self.get_display_name(tweak_name)
                
                value = ""
                if tweak_name in self.tweak_info:
                    tweak_info = self.tweak_info[tweak_name]
                    if tweak_info.get("type") in ["float", "int"]:
                        if hasattr(tweak, 'statustext') and tweak.statustext:
                            import re
                            match = re.search(r'\(([^)]+)\)', tweak.statustext)
                            if match:
                                value = f" = {match.group(1)}"
                
                active_tweaks.append((display_name, value))
        
        self.active_title.config(text=f"Active Tweaks ({len(active_tweaks)})")
        
        if not active_tweaks:
            no_tweaks_label = ttk.Label(self.active_tweaks_frame, text="No tweaks active", 
                                       font=("Arial", 15, "bold"), foreground="gray")
            no_tweaks_label.pack(pady=(20, 5))
            
            help_label = ttk.Label(self.active_tweaks_frame, text="Enable one using options to the left", 
                                   font=("Arial", 12), foreground="gray")
            help_label.pack()
        else:
            active_canvas = tk.Canvas(self.active_tweaks_frame, height=300)
            active_scrollbar = ttk.Scrollbar(self.active_tweaks_frame, orient="vertical", command=active_canvas.yview)
            active_content_frame = ttk.Frame(active_canvas)
            
            active_content_frame.bind(
                "<Configure>",
                lambda e: active_canvas.configure(scrollregion=active_canvas.bbox("all"))
            )
            
            active_canvas.create_window((0, 0), window=active_content_frame, anchor="nw")
            active_canvas.configure(yscrollcommand=active_scrollbar.set)
            
            active_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            active_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            for i, (display_name, value) in enumerate(active_tweaks):
                tweak_frame = ttk.Frame(active_content_frame)
                tweak_frame.pack(fill=tk.X, padx=5, pady=2)
                
                name_label = ttk.Label(tweak_frame, text=display_name, font=("Arial", 12, "bold"))
                name_label.pack(anchor=tk.W)
                
                if value:
                    value_label = ttk.Label(tweak_frame, text=value, font=("Arial", 11), foreground="blue")
                    value_label.pack(anchor=tk.W, padx=(10, 0))
                
                if i < len(active_tweaks) - 1:
                    separator = ttk.Separator(tweak_frame, orient='horizontal')
                    separator.pack(fill=tk.X, pady=5)
    
    def get_display_name(self, tweak_name):
        display_names = {
            "horseHack": "Horse speed restriction removed",
            "infiniteBoatRowStamina": "Infinite boat stamina enabled",
            "infiniteBreathUnderwater": "Infinite breath underwater enabled",
            "customXPMultiplier": "XP multiplier active",
            "customHealingReduction1": "Custom healing factor active",
            "customHealingReduction2": "Custom health boosts active",
            "customResourceLootModifier2": "Resource loot modifier active",
            "customDrachmaeMultiplier": "Drachmae multiplier active",
            "customTamedAnimalHealthBoost2": "Animal companion health boost active",
            "customTamedAnimalInCombatHealing": "Animal combat healing enabled",
            "customTamedAnimalHealingMultiplier2": "Animal healing multiplier active",
            "customEnemyHealthMultiplier": "Enemy health modifier active",
            "customEnemyDamageMultiplier": "Enemy damage modifier active",
            "customMaxEnemyLevelDelta": "Enemy level delta active",
            "customReducedBountyCooldown": "Reduced bounty cooldown active",
            "customDisableRegionLevels1": "Region levels disabled"
        }
        return display_names.get(tweak_name, tweak_name)
    
    def show_loading_dialog(self, operation, tweak_name):
        """Show a loading dialog during tweak operations"""
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Applying Tweak")
        loading_window.geometry("300x100")
        loading_window.resizable(False, False)
        loading_window.transient(self.root)
        loading_window.grab_set()
        
        loading_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        message = f"{operation} {tweak_name}..."
        message_label = ttk.Label(loading_window, text=message, font=("Arial", 10))
        message_label.pack(pady=20)
        
        progress = ttk.Progressbar(loading_window, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        loading_window.update()
        
        return loading_window
    
    def enable_tweak(self, tweak_name):
        if not self.fileName:
            messagebox.showerror("Error", "No game file selected")
            return
        
        if tweak_name not in self.tweaks:
            messagebox.showerror("Error", f"Tweak {tweak_name} not found")
            return
        
        tweak = self.tweaks[tweak_name]
        tweak_info = self.tweak_info.get(tweak_name, {})
        
        if tweak.status == 'Inactive':
            try:
                if tweak_info.get("type") == "bool":
                    loading_window = self.show_loading_dialog("Enabling", tweak_name)
                    try:
                        self.apply_simple_tweak(tweak_name)
                    finally:
                        loading_window.destroy()
                elif tweak_info.get("type") in ["float", "int"]:
                    self.prompt_for_value_and_apply(tweak_name, tweak_info)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to enable {tweak_name}: {str(e)}")
        else:
            messagebox.showinfo("Info", f"{tweak_name} is already active")
    
    def change_tweak_value(self, tweak_name):
        """Change the value of an active tweak"""
        if not self.fileName:
            messagebox.showerror("Error", "No game file selected")
            return
        
        if tweak_name not in self.tweaks:
            messagebox.showerror("Error", f"Tweak {tweak_name} not found")
            return
        
        tweak = self.tweaks[tweak_name]
        tweak_info = self.tweak_info.get(tweak_name, {})
        
        if tweak.status != 'Active':
            messagebox.showinfo("Info", f"{tweak_name} is not active")
            return
        
        if tweak_info.get("type") not in ["float", "int"]:
            messagebox.showinfo("Info", f"{tweak_name} does not support value changes")
            return
        
        self.prompt_for_value_and_apply(tweak_name, tweak_info, is_change=True)
    
    def disable_tweak(self, tweak_name):
        if not self.fileName:
            messagebox.showerror("Error", "No game file selected")
            return
        
        if tweak_name not in self.tweaks:
            messagebox.showerror("Error", f"Tweak {tweak_name} not found")
            return
        
        tweak = self.tweaks[tweak_name]
        
        if tweak.status == 'Active':
            loading_window = self.show_loading_dialog("Disabling", tweak_name)
            
            try:
                tweak.Disable()
                self.update_all_status()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to disable {tweak_name}: {str(e)}")
            finally:
                loading_window.destroy()
        else:
            messagebox.showinfo("Info", f"{tweak_name} is not active")
    
    def apply_simple_tweak(self, tweak_name):
        try:
            tweak = self.tweaks[tweak_name]
            tweak.Enable()
            
            if tweak_name == "infiniteBoatRowStamina":
                self.tweaks["infiniteBoatRowStamina2"].Enable()
            elif tweak_name == "infiniteBreathUnderwater":
                self.tweaks["infiniteBreathUnderwater2"].Enable()
            elif tweak_name == "customDisableRegionLevels1":
                self.tweaks["customDisableRegionLevels2"].Enable()
            
            self.update_all_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable {tweak_name}: {str(e)}")
    
    def prompt_for_value_and_apply(self, tweak_name, tweak_info, is_change=False):
        """Prompt user for value input and apply the tweak"""
        value_type = tweak_info.get("type")
        min_val = tweak_info.get("min")
        max_val = tweak_info.get("max")
        
        dialog = tk.Toplevel(self.root)
        if is_change:
            dialog.title(f"Change Value for {self.get_display_name(tweak_name)}")
        else:
            dialog.title(f"Enter Value for {self.get_display_name(tweak_name)}")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        if is_change:
            description_text = f"Please enter a new value for {self.get_display_name(tweak_name)}:"
        else:
            description_text = f"Please enter a value for {self.get_display_name(tweak_name)}:"
        if min_val is not None and max_val is not None:
            description_text += f"\nValid range: {min_val} to {max_val}"
        elif min_val is not None:
            description_text += f"\nMinimum value: {min_val}"
        elif max_val is not None:
            description_text += f"\nMaximum value: {max_val}"
        
        if value_type == "float":
            description_text += "\nNumber can be a whole number or decimal (e.g., 2.5)"
        elif value_type == "int":
            description_text += "\nEnter a whole number with no decimal places (e.g., 2)"
        
        desc_label = ttk.Label(frame, text=description_text, wraplength=350)
        desc_label.pack(pady=(0, 10))
        
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT)
        
        value_var = tk.StringVar()
        if value_type == "float":
            if min_val is not None:
                value_var.set(str(min_val))
            else:
                value_var.set("1.0")
        elif value_type == "int":
            if min_val is not None:
                value_var.set(str(min_val))
            else:
                value_var.set("1")
        
        entry = ttk.Entry(input_frame, textvariable=value_var, width=20)
        entry.pack(side=tk.LEFT, padx=(5, 0))
        entry.focus_set()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(20, 0))
        
        result = {"value": None, "cancelled": False}
        
        def on_ok():
            try:
                value_str = value_var.get().strip()
                if not value_str:
                    messagebox.showerror("Error", "Please enter a value", parent=dialog)
                    return
                
                if value_type == "float":
                    value = float(value_str)
                elif value_type == "int":
                    value = int(value_str)
                else:
                    value = float(value_str)
                
                if min_val is not None and value < min_val:
                    messagebox.showerror("Error", f"Value must be at least {min_val}", parent=dialog)
                    return
                if max_val is not None and value > max_val:
                    messagebox.showerror("Error", f"Value must be at most {max_val}", parent=dialog)
                    return
                
                result["value"] = value
                dialog.destroy()
                
            except ValueError:
                if value_type == "float":
                    messagebox.showerror("Error", "Please enter a valid decimal number", parent=dialog)
                elif value_type == "int":
                    messagebox.showerror("Error", "Please enter a valid whole number", parent=dialog)
                else:
                    messagebox.showerror("Error", "Please enter a valid number", parent=dialog)
        
        def on_cancel():
            result["cancelled"] = True
            dialog.destroy()
        
        def on_enter(event):
            on_ok()
        
        entry.bind('<Return>', on_enter)
        
        if is_change:
            ttk.Button(button_frame, text="Change", style='Large.TButton', command=on_ok).pack(side=tk.LEFT, padx=(0, 10))
        else:
            ttk.Button(button_frame, text="OK", style='Large.TButton', command=on_ok).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", style='Large.TButton', command=on_cancel).pack(side=tk.LEFT)
        
        dialog.wait_window()
        
        if result["cancelled"]:
            return
        
        if is_change:
            loading_window = self.show_loading_dialog("Changing", tweak_name)
        else:
            loading_window = self.show_loading_dialog("Enabling", tweak_name)
        try:
            self.apply_value_tweak(tweak_name, tweak_info, result["value"])
        finally:
            loading_window.destroy()
    
    def apply_value_tweak(self, tweak_name, tweak_info, value):
        """Apply a tweak with a specific value"""
        try:
            value_type = tweak_info.get("type")
            
            min_val = tweak_info.get("min")
            max_val = tweak_info.get("max")
            
            if min_val is not None and value < min_val:
                messagebox.showerror("Error", f"Value must be at least {min_val}")
                return
            if max_val is not None and value > max_val:
                messagebox.showerror("Error", f"Value must be at most {max_val}")
                return
            
            tweak = self.tweaks[tweak_name]
            
            was_active = tweak.status == 'Active'
            if was_active:
                tweak.Disable()
            
            if value_type == "float":
                temp = BitArray(floatle=value, length=32)
            else:
                temp = BitArray(uint=value, length=8)
            
            temp2 = BitArray(tweak.modifiedByteArray)
            temp2.overwrite(temp, tweak.variableOffset * 4)
            tweak.modifiedByteArray = '0x' + temp2.hex
            tweak.Enable()
            
            if tweak_name == "customXPMultiplier":
                if value < 1.0:
                    self.tweaks["customXPMultiplierDisableLowerBound1"].Enable()
                    self.tweaks["customXPMultiplierDisableLowerBound2"].Enable()
                    self.tweaks["customXPMultiplierDisableLowerBound3"].Enable()
                    self.tweaks["customXPMultiplierDisableLowerBound4"].Enable()
                else:
                    self.tweaks["customXPMultiplierDisableLowerBound1"].Disable()
                    self.tweaks["customXPMultiplierDisableLowerBound2"].Disable()
                    self.tweaks["customXPMultiplierDisableLowerBound3"].Disable()
                    self.tweaks["customXPMultiplierDisableLowerBound4"].Disable()
            
            elif tweak_name == "customDrachmaeMultiplier":
                if value < 1.0:
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound1"].Enable()
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound2"].Enable()
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound3"].Enable()
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound4"].Enable()
                else:
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound1"].Disable()
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound2"].Disable()
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound3"].Disable()
                    self.tweaks["customDrachmaeMultiplierDisableLowerBound4"].Disable()
            
            elif tweak_name == "customResourceLootModifier2":
                self.tweaks["customResourceLootModifier1"].Enable()
            
            elif tweak_name == "customTamedAnimalHealthBoost2":
                self.tweaks["customTamedAnimalHealthBoost1"].Enable()
            
            elif tweak_name == "customTamedAnimalHealingMultiplier2":
                self.tweaks["customTamedAnimalHealingMultiplier1"].Enable()
            
            self.update_all_status()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable {tweak_name}: {str(e)}")
    
    def run_game(self):
        if self.fileName and os.path.exists(self.fileName):
            os.startfile(self.fileName)
        else:
            messagebox.showerror("Error", "Game file not found")
    
    def create_backup(self):
        if not self.fileName:
            messagebox.showerror("Error", "No game file selected")
            return
        
        if NumActiveTweaks(self.tweaks) > 0:
            messagebox.showwarning("Warning", "There are active tweaks. Disable them before creating a backup.")
            return
        
        try:
            backup_dir = os.path.dirname(os.path.abspath(self.fileName))
            backup_file = backup_dir + os.path.sep + 'ACOdyssey.exe.backup'
            copyfile(self.fileName, backup_file)
            self.backup_exists = True
            messagebox.showinfo("Success", "Backup created successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
    
    def restore_backup(self):
        if not self.backup_exists:
            messagebox.showerror("Error", "No backup found")
            return
        
        try:
            backup_dir = os.path.dirname(os.path.abspath(self.fileName))
            backup_file = backup_dir + os.path.sep + 'ACOdyssey.exe.backup'
            copyfile(backup_file, self.fileName)
            self.initialize_tweaks()
            messagebox.showinfo("Success", "Backup restored successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore backup: {str(e)}")
    
    def disable_all(self):
        if NumActiveTweaks(self.tweaks) == 0:
            messagebox.showinfo("Info", "No active tweaks to disable")
            return
        
        try:
            for tweak_name in self.tweaks:
                tweak = self.tweaks.get(tweak_name)
            if isinstance(tweak, cByteArrayHack) and tweak.status == 'Active':
                tweak.Disable()
    
            self.update_all_status()
            messagebox.showinfo("Success", "All tweaks disabled successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disable all tweaks: {str(e)}")
    
    def refresh_status(self):
        if self.fileName:
            self.initialize_tweaks()
        else:
            messagebox.showerror("Error", "No game file selected")
    
    def open_nexus_page(self, event=None):
        """Open the Nexus Mods page for this mod"""
        import webbrowser
        url = "https://www.nexusmods.com/assassinscreedodyssey/mods/12"
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open browser: {str(e)}")
    
    def show_help(self, tweak_name):
        """Show help information for a specific tweak"""
        help_info = {
            "horseHack": {
                "title": "Disable Horse Speed Restriction",
                "description": "This removes the forced horse speed cap when approaching towns and cities."
            },
            "infiniteBoatRowStamina": {
                "title": "Infinite Boat Row Stamina",
                "description": "Removes stamina consumption when rowing boats, allowing unlimited rowing."
            },
            "infiniteBreathUnderwater": {
                "title": "Infinite Breath Underwater",
                "description": "Prevents the breath meter from depleting when swimming underwater, allowing unlimited underwater exploration."
            },
            "customXPMultiplier": {
                "title": "Custom XP Multiplier",
                "description": "This sets the master XP multiplier. You can check this is active as there should be a little yellow circle next to the XP bar when in the menu in the game. This can be used to enable and disable the multiplier.\n\nI have the XP Boost active, so I need to check that others can see this. Theoretically it should appear when the multiplier is set."
            },
            "customEnemyHealthMultiplier": {
                "title": "Custom Enemy Health Multiplier",
                "description": "This multiplier defines how much health melee opponents will have. Doesn't affect ships."
            },
            "customEnemyDamageMultiplier": {
                "title": "Custom Enemy Damage Multiplier",
                "description": "This multiplier defines how much damage melee opponents will do. Doesn't affect ships."
            },
            "customMaxEnemyLevelDelta": {
                "title": "Custom Max Enemy Level Delta",
                "description": "This sets the maximum level the player can out-level areas and opponent. It basically configures the whole scaling mechanism. So setting it to 100 for example effectively disables auto scaling altogether.\n\nNotes:\n• Cultists and Mercenaries will always be spawned at their set level.\n• Neutral opponents such as civilians will always turn hostile at the player level.\n• Attika will always have an upper level equal to the player level."
            },
            "customDrachmaeMultiplier": {
                "title": "Custom Drachmae Multiplier",
                "description": "This permits the customisation of drachmae rewards, including random loot. Values less than 1.00 permitted if users want to tone down drachmae rewards."
            },
            "customHealingReduction1": {
                "title": "Custom Healing : Out Of Combat Alternative",
                "description": "Experimental tweak to out of combat healing. The purpose of this tweak is to increase challenge and reduce players' ability to simply run away and heal.\n\nPlayers can now set a healing factor between 1 and 15. 1 means almost instant healing, 15 will effectively disable healing. The tweak was previously set to a default of 10.\n\nOut of combat healing is affected by this factor and is proportionate to the amount of health remaining. Less health = slower healing. Taking too much damage can result in health not being able to recover at all.\n\nThere will always be a very gradual amount if healing whilst mounted and players can also heal when fast travelling.\n\nThe ability to heal will start fast, then trail off and then gradually increase as the player levels up, however what is observed will be dependent on what the player sets this factor at, so players are encouraged to experiment."
            },
            "customHealingReduction2": {
                "title": "Custom Healing : Reduced Health Boosts",
                "description": "This reduces the health awarded when using adrenaline based abilities as well as when using the second wind ability."
            },
            "customResourceLootModifier2": {
                "title": "Custom Resource Loot Modifier",
                "description": "The amount of resources received when looting can be modified using this tweak. Amounts are scaled by a factor of 2, so setting this to 1 gives 1×2 = 2 times the amount. Setting to 5 yields 1×2×2×2×2×2 = 32 times the amount. So the player can choose from 2, 4, 8, 16 and 32 times the rewards respectively.\n\nThis applies to all resources except drachmae which has its own dedicated modifier."
            },
            "customTamedAnimalHealthBoost2": {
                "title": "Animal Companion : Health Boost",
                "description": "A tamed animal's max health will be set according to the multiplier the player defines. This stacks with other animal HP bonuses. So an animal with base health 5,000, a 1.5x multiplier and +100% health engraving = 5,000×1.5×2.0 = 15,000hp."
            },
            "customTamedAnimalInCombatHealing": {
                "title": "Animal Companion : In Combat Healing",
                "description": "Allows tamed animals to heal whilst in combat."
            },
            "customTamedAnimalHealingMultiplier2": {
                "title": "Animal Companion : Healing Multiplier",
                "description": "Sets how quickly tamed animals heal. It's usually quite fast, to slow it down ranges between 0.1 and 0.5 are recommended."
            },
            "customReducedBountyCooldown": {
                "title": "Reduced Bounty Cooldown",
                "description": "This doubles the cooldown speed for player bounties. It's intended for those who don't like simply paying off bounties and would rather go after bounty sponsors or otherwise feel consequences."
            },
            "customDisableRegionLevels1": {
                "title": "Disable Region Levels",
                "description": "Sets all regions to the player level, and therefore also makes all content based on region level the same level as the player therefore removing the level gating in the game. Makes the world truly open for players to explore at will rather than only being able to tackle sections at the player level. Regions are now difficult because of the enemy types rather than artificial 'level' difficulty, as they should be. The result is a much more balanced and open game. Mercenaries will still be at their default levels and quests still appear at their base levels - I haven't tested quest-specific content. From the testing that has been done, some challenging content will still be a level above the player, which isn't unreasonable."
            }
        }
        
        if tweak_name in help_info:
            info = help_info[tweak_name]
            messagebox.showinfo(f"Help - {info['title']}", info['description'])
        else:
            messagebox.showinfo("Help", "No help information available for this tweak.")

DisplayWelcomeMessage()

if __name__ == "__main__":
    root = tk.Tk()
    app = ACOdysseyTweakPackGUI(root)
    root.mainloop()
