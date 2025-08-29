# all credits to https://next.nexusmods.com/profile/vahndaar

import errno
import os
import sys
import winreg
import platform
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

NUM_TWEAKS = 26
CURRENT_VERSION = 'V1.0.2.3'
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
    print('1.  Disable Horse Speed Restriction\t\t', tweaks['horseHack'].statustext)
    print('2.  Custom XP Multiplier\t\t\t', tweaks['customXPMultiplier'].statustext)
    print('3.  Custom Enemy Health Multiplier\t\t', tweaks['customEnemyHealthMultiplier'].statustext)
    print('4.  Custom Enemy Damage Multiplier\t\t', tweaks['customEnemyDamageMultiplier'].statustext)
    print('5.  Custom Max Enemy Level Delta\t\t', tweaks['customMaxEnemyLevelDelta'].statustext)
    print('6.  Custom Drachmae Multiplier\t\t\t', tweaks['customDrachmaeMultiplier'].statustext)
    print('7.  Custom Healing : Healing Factor\t\t', tweaks['customHealingReduction1'].statustext)
    print('8.  Custom Healing : Reduced Health Boosts\t', tweaks['customHealingReduction2'].statustext)
    print('9.  Custom Resource Loot Modifier\t\t', tweaks['customResourceLootModifier2'].statustext)
    print('10. Animal Companion : Health Boost\t\t', tweaks['customTamedAnimalHealthBoost2'].statustext)
    print('11. Animal Companion : In Combat Healing\t', tweaks['customTamedAnimalInCombatHealing'].statustext)
    print('12. Animal Companion : Healing Multiplier\t', tweaks['customTamedAnimalHealingMultiplier2'].statustext)
    print('13. Reduced Bounty Cooldown\t\t\t', tweaks['customReducedBountyCooldown'].statustext)
    print('14. Disable Region Levels\t\t\t', tweaks['customDisableRegionLevels1'].statustext)
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
    customResourceLootModifier2 = cByteArrayHack('Custom Resource Loot Modifier Patch 2', fileName, '0x488B5C24304883C4205FC3CCCCCCCCE93B49F30DCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC', '0x488B5C24304883C4205FC3CCCCCCCCE93BB5E90DCCCCCCB80000C03F660F6ED0F30F59C2F3480F2CC8B801000000E99130E9FF', 48, 'float')
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
    print()
    tweak_collection = {'horseHack': horseHack, 'customDrachmaeMultiplier': customDrachmaeMultiplier, 'customDrachmaeMultiplierDisableLowerBound1': customDrachmaeMultiplierDisableLowerBound1, 'customDrachmaeMultiplierDisableLowerBound2': customDrachmaeMultiplierDisableLowerBound2, 'customDrachmaeMultiplierDisableLowerBound3': customDrachmaeMultiplierDisableLowerBound3, 'customDrachmaeMultiplierDisableLowerBound4': customDrachmaeMultiplierDisableLowerBound4, 'customXPMultiplier': customXPMultiplier, 'customXPMultiplierDisableLowerBound1': customXPMultiplierDisableLowerBound1, 'customXPMultiplierDisableLowerBound2': customXPMultiplierDisableLowerBound2, 'customXPMultiplierDisableLowerBound3': customXPMultiplierDisableLowerBound3, 'customXPMultiplierDisableLowerBound4': customXPMultiplierDisableLowerBound4, 'customEnemyHealthMultiplier': customEnemyHealthMultiplier, 'customEnemyDamageMultiplier': customEnemyDamageMultiplier, 'customMaxEnemyLevelDelta': customMaxEnemyLevelDelta, 'customHealingReduction1': customHealingReduction1, 'customHealingReduction2': customHealingReduction2, 'customResourceLootModifier1': customResourceLootModifier1, 'customResourceLootModifier2': customResourceLootModifier2, 'customTamedAnimalHealthBoost1': customTamedAnimalHealthBoost1, 'customTamedAnimalHealthBoost2': customTamedAnimalHealthBoost2, 'customTamedAnimalInCombatHealing': customTamedAnimalInCombatHealing, 'customTamedAnimalHealingMultiplier1': customTamedAnimalHealingMultiplier1, 'customTamedAnimalHealingMultiplier2': customTamedAnimalHealingMultiplier2, 'customReducedBountyCooldown': customReducedBountyCooldown, 'customDisableRegionLevels1': customDisableRegionLevels1, 'customDisableRegionLevels2': customDisableRegionLevels2}
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

def GetExeFile():
    print('Searching for game executable...', end='')
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
        print('ACOdyssey.exe found here : ' + fileName)
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
    
    # Check if the input is a directory and look for ACOdyssey.exe within it
    if os.path.isdir(fileName):
        potential_exe = os.path.join(fileName, 'ACOdyssey.exe')
        if os.path.isfile(potential_exe):
            print(f'Found ACOdyssey.exe in directory: {potential_exe}')
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
DisplayWelcomeMessage()
fileName = GetExeFile()
tweaks = InitialiseTweaks(fileName)
backup_exists = CheckForBackup(fileName)
keyed_input = ''

while keyed_input != 'X' and keyed_input != 'x':
    WriteMenu(tweaks, CheckForBackup(fileName))
    keyed_input = input('Please select an option: ')
    
    if keyed_input == '1':
        tweak = tweaks['horseHack']
        if tweak.status == 'Inactive':
            tweak.Enable()
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '2':
        tweak = tweaks['customXPMultiplier']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set multiplier value to : '))
                if new_value < 0.0:
                    print('Cannot be less than 0.')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
                if new_value < 1.0:
                    print('Value < 1.00, disabling lower multiplier limits...')
                    tweaks['customXPMultiplierDisableLowerBound1'].Enable()
                    tweaks['customXPMultiplierDisableLowerBound2'].Enable()
                    tweaks['customXPMultiplierDisableLowerBound3'].Enable()
                    tweaks['customXPMultiplierDisableLowerBound4'].Enable()
                else:
                    tweaks['customXPMultiplierDisableLowerBound1'].Disable()
                    tweaks['customXPMultiplierDisableLowerBound2'].Disable()
                    tweaks['customXPMultiplierDisableLowerBound3'].Disable()
                    tweaks['customXPMultiplierDisableLowerBound4'].Disable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
            tweaks['customXPMultiplierDisableLowerBound1'].Disable()
            tweaks['customXPMultiplierDisableLowerBound2'].Disable()
            tweaks['customXPMultiplierDisableLowerBound3'].Disable()
            tweaks['customXPMultiplierDisableLowerBound4'].Disable()
    
    elif keyed_input == '3':
        tweak = tweaks['customEnemyHealthMultiplier']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set enemy health multiplier to : '))
                if new_value < 0.0:
                    print('Cannot be less than 0.')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '4':
        tweak = tweaks['customEnemyDamageMultiplier']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set enemy damage multiplier to : '))
                if new_value < 0.0:
                    print('Cannot be less than 0.')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '5':
        tweak = tweaks['customMaxEnemyLevelDelta']
        if tweak.status == 'Inactive':
            try:
                new_value = int(input('Set max delta to (0-255) : '))
                if new_value < 0 or new_value > 255:
                    print('Only whole numbers in the range 0 - 255 accepted!')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(uint=new_value, length=8)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
            except ValueError:
                print('Only whole numbers in the range 0 - 255 accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '6':
        tweak = tweaks['customDrachmaeMultiplier']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set multiplier value to : '))
                if new_value < 0.0:
                    print('Cannot be less than 0.')
                    k = input('Press a key to continue...')
                    continue
                if new_value < 0.5:
                    print('Setting less than 0.5 may result in some loot awarding no drachmae.')
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
                if new_value < 1.0:
                    print('Value < 1.00, disabling lower multiplier limits...')
                    tweaks['customDrachmaeMultiplierDisableLowerBound1'].Enable()
                    tweaks['customDrachmaeMultiplierDisableLowerBound2'].Enable()
                    tweaks['customDrachmaeMultiplierDisableLowerBound3'].Enable()
                    tweaks['customDrachmaeMultiplierDisableLowerBound4'].Enable()
                else:
                    tweaks['customDrachmaeMultiplierDisableLowerBound1'].Disable()
                    tweaks['customDrachmaeMultiplierDisableLowerBound2'].Disable()
                    tweaks['customDrachmaeMultiplierDisableLowerBound3'].Disable()
                    tweaks['customDrachmaeMultiplierDisableLowerBound4'].Disable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
            tweaks['customDrachmaeMultiplierDisableLowerBound1'].Disable()
            tweaks['customDrachmaeMultiplierDisableLowerBound2'].Disable()
            tweaks['customDrachmaeMultiplierDisableLowerBound3'].Disable()
            tweaks['customDrachmaeMultiplierDisableLowerBound4'].Disable()
    
    elif keyed_input == '7':
        tweak = tweaks['customHealingReduction1']
        if tweak.status == 'Inactive':
            try:
                new_value = int(input('Set healing factor (1-15): '))
                if new_value < 1 or new_value > 15:
                    print('Only whole numbers in the range 1 - 15 accepted!')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(uint=new_value, length=8)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
            except ValueError:
                print('Only whole numbers in the range 1 - 15 accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '8':
        tweak = tweaks['customHealingReduction2']
        if tweak.status == 'Inactive':
            try:
                new_value = int(input('Set health boost reduction factor to (1-5) : '))
                if new_value < 1 or new_value > 5:
                    print('Only whole numbers in the range 1 - 5 accepted!')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(uint=new_value, length=8)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweak.Enable()
            except ValueError:
                print('Only whole numbers in the range 1 - 5 accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '9':
        tweak = tweaks['customResourceLootModifier2']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set resource loot scaling factor to : '))
                if new_value < 1.0:
                    print('Cannot be less than 1.')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweaks['customResourceLootModifier1'].Enable()
                tweak.Enable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweaks['customResourceLootModifier1'].Disable()
            tweak.Disable()
    
    elif keyed_input == '10':
        tweak = tweaks['customTamedAnimalHealthBoost2']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set animal companion health multiplier to : '))
                if new_value < 1.0:
                    print('Cannot be less than 1.')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweaks['customTamedAnimalHealthBoost1'].Enable()
                tweak.Enable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweaks['customTamedAnimalHealthBoost1'].Disable()
            tweak.Disable()
    
    elif keyed_input == '11':
        tweak = tweaks['customTamedAnimalInCombatHealing']
        if tweak.status == 'Inactive':
            tweak.Enable()
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '12':
        tweak = tweaks['customTamedAnimalHealingMultiplier2']
        if tweak.status == 'Inactive':
            try:
                new_value = float(input('Set animal companion healing multiplier to : '))
                if new_value < 0.0:
                    print('Cannot be less than 0.')
                    k = input('Press a key to continue...')
                    continue
                temp = BitArray(floatle=new_value, length=32)
                temp2 = BitArray(tweak.modifiedByteArray)
                temp2.overwrite(temp, tweak.variableOffset * 4)
                tweak.modifiedByteArray = '0x' + temp2.hex
                tweaks['customTamedAnimalHealingMultiplier1'].Enable()
                tweak.Enable()
            except ValueError:
                print('Only numerical values accepted!')
                k = input('Press a key to continue...')
        elif tweak.status == 'Active':
            tweaks['customTamedAnimalHealingMultiplier1'].Disable()
            tweak.Disable()
    
    elif keyed_input == '13':
        tweak = tweaks['customReducedBountyCooldown']
        if tweak.status == 'Inactive':
            tweak.Enable()
        elif tweak.status == 'Active':
            tweak.Disable()
    
    elif keyed_input == '14':
        tweak = tweaks['customDisableRegionLevels1']
        if tweak.status == 'Inactive':
            tweak.Enable()
            tweaks['customDisableRegionLevels2'].Enable()
        elif tweak.status == 'Active':
            tweak.Disable()
            tweaks['customDisableRegionLevels2'].Disable()
    
    elif keyed_input == 'R' or keyed_input == 'r':
        os.startfile(fileName)
    
    elif keyed_input == 'L' or keyed_input == 'l':
        if CheckForBackup(fileName) == True:
            backup_dir = os.path.dirname(os.path.abspath(fileName))
            backup_file = backup_dir + os.path.sep + 'ACOdyssey.exe.backup'
            print('Restoring backup file...')
            try:
                copyfile(backup_file, fileName)
                tweaks = InitialiseTweaks(fileName)
            except IOError:
                print('Unable to restore backup. Ensure the file isn\'t in use and try again.')
                k = input('Press a key to continue...')
    
    elif (keyed_input == 'D' or keyed_input == 'd') and NumActiveTweaks(tweaks) > 0:
        for tweak_name in tweaks:
            tweak = tweaks.get(tweak_name)
            if isinstance(tweak, cByteArrayHack) and tweak.status == 'Active':
                tweak.Disable()
    
    elif keyed_input == 'S' or keyed_input == 's':
        if NumActiveTweaks(tweaks) == 0:
            SaveBackup(0, fileName)
    
    elif keyed_input == 'X' or keyed_input == 'x':
        k = input('Thanks for using this tool! Enjoy! VD')

k = input('Thanks for using this tool! Enjoy! VD')
