#!/usr/bin/env python3
import os
import sys
import re
import xml.etree.ElementTree as ET

def patch_advanced_xml(file_path):
    print(f"Memeriksa file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if "fox_other_additions" not in text or "listbox_group_additions" not in text:
        print(f"Skipping {file_path}: bukan format modern OrangeFox advanced.xml")
        return False

    # 1. Definisi susunan baru untuk grup 'Addition':
    # - Root Apps (Magisk, APatch, KernelSU)
    # - Terminal
    # - Copy Log to SD
    # - Other (membuka sub-halaman fox_other_additions)
    new_additions = '''<listbox style="group_list">
\t\t\t\t<placement x="0" y="%row5_1_y%" w="%screen_w%" h="%adv_additions_h%"/>
\t\t\t\t<listitem name="Magisk Manager">
\t\t\t\t\t<condition var1="fileexists" var2="%magisk_path%"/>
\t\t\t\t\t<condition var1="no_magisk" op="!=" var2="1"/>
\t\t\t\t\t<icon res="wand_shine"/>
\t\t\t\t\t<action function="set">rmm_found=-1</action>
\t\t\t\t\t<action function="set">rmm_type=magisk</action>
\t\t\t\t\t<action function="page">modules_mount</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="Magisk Manager">
\t\t\t\t\t<condition var1="fileexists" op="!=" var2="%magisk_path%"/>
\t\t\t\t\t<condition var1="fileexists" op="!=" var2="%ap_path%"/>
\t\t\t\t\t<condition var1="fileexists" op="!=" var2="%ksu_path%"/>
\t\t\t\t\t<condition var1="no_magisk" op="!=" var2="1"/>
\t\t\t\t\t<icon res="wand_shine"/>
\t\t\t\t\t<action function="set">rmm_found=-1</action>
\t\t\t\t\t<action function="set">rmm_type=magisk</action>
\t\t\t\t\t<action function="page">modules_mount</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@ap_modules}">
\t\t\t\t\t<condition var1="fileexists" var2="%ap_path%"/>
\t\t\t\t\t<icon res="android"/>
\t\t\t\t\t<action function="set">rmm_found=-1</action>
\t\t\t\t\t<action function="set">rmm_type=ap</action>
\t\t\t\t\t<action function="page">modules_mount</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@ksu_modules}">
\t\t\t\t\t<condition var1="fileexists" var2="%ksu_path%"/>
\t\t\t\t\t<icon res="kernelsu"/>
\t\t\t\t\t<action function="set">rmm_found=-1</action>
\t\t\t\t\t<action function="set">rmm_type=ksu</action>
\t\t\t\t\t<action function="page">modules_mount</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@terminal_btn}">
\t\t\t\t\t<icon res="terminal"/>
\t\t\t\t\t<action function="page">terminal</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@copy_log_btn}">
\t\t\t\t\t<icon res="overview"/>
\t\t\t\t\t<action function="set">tw_back=advanced</action>
\t\t\t\t\t<action function="set">tw_action=copylog</action>
\t\t\t\t\t<action function="set">tw_text1={@copy_log_confirm}</action>
\t\t\t\t\t<action function="set">tw_action_text1={@copy_log_btn}</action>
\t\t\t\t\t<action function="set">tw_action_text2={@copying_log}</action>
\t\t\t\t\t<action function="set">tw_complete_text1={@copy_log_complete}</action>
\t\t\t\t\t<action function="set">tw_slider_text={@swipe_to_confirm}</action>
\t\t\t\t\t<action function="page">confirm_action</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@cust_oth}">
\t\t\t\t\t<icon res="other"/>
\t\t\t\t\t<action function="page">fox_other_additions</action>
\t\t\t\t</listitem>
\t\t\t</listbox>'''

    # 2. Definisi susunan baru untuk halaman 'Other' (fox_other_additions):
    # - App Manager
    # - Fix Contexts
    # - Fox Addons
    # - Flash Current OrangeFox (reflashtwrp)
    # - Decrypt Data & Users
    # - Inject TWRP & Maintainer Settings
    new_other = '''<page name="fox_other_additions">
\t\t\t<listbox style="group_list">
\t\t\t\t<placement x="0" y="%ab_h%" w="%screen_w%" h="%files_np_w%"/>
\t\t\t\t<listitem name="{@appmgr_title}">
\t\t\t\t\t<condition var1="enable_app_manager" var2="1"/>
\t\t\t\t\t<icon res="apps_box"/>
\t\t\t\t\t<action function="page">apps_load</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@fix_contexts_hdr}">
\t\t\t\t\t<condition var1="tw_has_data_media" var2="1"/>
\t\t\t\t\t<icon res="build"/>
\t\t\t\t\t<action function="page">fixcontexts</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@fox_modules_hdr}">
\t\t\t\t\t<condition var1="fileexists" var2="/FFiles/OF_reset/OF_reset.zip"/>
\t\t\t\t\t<icon res="addons"/>
\t\t\t\t\t<action function="page">fox_modules</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@reflash_twrp}">
\t\t\t\t\t<icon res="wrench"/>
\t\t\t\t\t<condition var1="fox_branch" op="&gt;=" var2="11"/>
\t\t\t\t\t<condition var1="fox_disable_reflash_current" op="!=" var2="1"/>
\t\t\t\t\t<action function="set">tw_repack_kernel=0</action>
\t\t\t\t\t<action function="set">tw_back=fox_other_additions</action>
\t\t\t\t\t<action function="set">tw_action=reflashtwrp</action>
\t\t\t\t\t<action function="set">tw_text1={@reflash_twrp}</action>
\t\t\t\t\t<action function="set">tw_action_text1={@reflashing_twrp}</action>
\t\t\t\t\t<action function="set">tw_complete_text1={@reflash_twrp_complete}</action>
\t\t\t\t\t<action function="set">tw_slider_text={@swipe_to_confirm}</action>
\t\t\t\t\t<action function="page">confirm_action</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@decrypt_data_btn}">
\t\t\t\t\t<condition var1="tw_is_fbe" op="!=" var2="1"/>
\t\t\t\t\t<condition var1="tw_is_encrypted" var2="1"/>
\t\t\t\t\t<condition var1="tw_is_decrypted" var2="0"/>
\t\t\t\t\t<icon res="key"/>
\t\t\t\t\t<action function="set">tw_crypto_user_id=0</action>
\t\t\t\t\t<action function="set">tw_crypto_password=</action>
\t\t\t\t\t<action function="set">tw_password_fail=0</action>
\t\t\t\t\t<action function="set">tw_crypto_pwtype=%tw_crypto_pwtype_0%</action>
\t\t\t\t\t<action function="set">of_decrypt_from_menu=1</action>
\t\t\t\t\t<action function="page">decrypt</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@decrypt_users}">
\t\t\t\t\t<condition var1="tw_is_fbe" var2="1"/>
\t\t\t\t\t<condition var1="tw_all_users_decrypted" var2="0"/>
\t\t\t\t\t<icon res="key"/>
\t\t\t\t\t<action function="page">decrypt_users</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@inject_twrp_btn}">
\t\t\t\t\t<condition var1="tw_has_injecttwrp" var2="1"/>
\t\t\t\t\t<icon res="build"/>
\t\t\t\t\t<action function="set">tw_back=fox_other_additions</action>
\t\t\t\t\t<action function="set">tw_action=reinjecttwrp</action>
\t\t\t\t\t<action function="set">tw_text1={@inject_twrp_confirm}</action>
\t\t\t\t\t<action function="set">tw_action_text1={@injecting_twrp}</action>
\t\t\t\t\t<action function="set">tw_complete_text1={@inject_twrp_complete}</action>
\t\t\t\t\t<action function="set">tw_slider_text={@swipe_to_confirm}</action>
\t\t\t\t\t<action function="page">confirm_action</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@fix_recovery_loop}">
\t\t\t\t\t<icon res="build"/>
\t\t\t\t\t<condition var1="tw_has_boot_slots" var2="1"/>
\t\t\t\t\t<condition var1="tw_has_repack_tools" var2="1"/>
\t\t\t\t\t<condition var1="tw_uses_initramfs" var2="1"/>
\t\t\t\t\t<action function="set">tw_back=fox_other_additions</action>
\t\t\t\t\t<action function="set">tw_action=fixabrecoverybootloop</action>
\t\t\t\t\t<action function="set">tw_text1={@fix_recovery_loop}</action>
\t\t\t\t\t<action function="set">tw_action_text1={@fixing_recovery_loop}</action>
\t\t\t\t\t<action function="set">tw_complete_text1={@fix_recovery_loop_complete}</action>
\t\t\t\t\t<action function="set">tw_slider_text={@swipe_to_confirm}</action>
\t\t\t\t\t<action function="page">confirm_action</action>
\t\t\t\t</listitem>
\t\t\t\t<listitem name="{@custom_settings}">
\t\t\t\t\t<condition var1="fileexists" var2="/sbin/maintainer.xml"/>
\t\t\t\t\t<icon res="home_repair_service"/>
\t\t\t\t\t<action function="page">maintainer</action>
\t\t\t\t</listitem>
\t\t\t</listbox>'''

    pattern1 = r'(<text style="caption">\s*<placement x="%gl_text_x%" y="%row4_3_y%"/>\s*<text>\{@listbox_group_additions\}</text>\s*</text>\s*)<listbox style="group_list">.*?</listbox>'
    text_mod = re.sub(pattern1, r'\g<1>' + new_additions, text, flags=re.DOTALL)
    if text_mod == text:
        # Coba pattern yang lebih fleksibel jika placement koordinat berbeda
        pattern1_alt = r'(<text[^>]*>\{@listbox_group_additions\}</text>\s*</text>\s*)<listbox style="group_list">.*?</listbox>'
        text_mod = re.sub(pattern1_alt, r'\g<1>' + new_additions, text, flags=re.DOTALL)

    pattern2 = r'<page name="fox_other_additions">\s*<listbox style="group_list">.*?</listbox>'
    text_mod2 = re.sub(pattern2, new_other, text_mod, flags=re.DOTALL)

    # Validasi bahwa XML tetap valid
    try:
        ET.fromstring(text_mod2)
        print(f"Validasi XML berhasil untuk {file_path}")
    except Exception as e:
        print(f"Error memvalidasi XML hasil modifikasi: {e}")
        return False

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text_mod2)

    print(f"Berhasil memperbarui menu dan sub-halaman di {file_path}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: rearrange_menu.py <FOX_DIR>")
        sys.exit(1)

    fox_dir = sys.argv[1]
    gui_dir = os.path.join(fox_dir, "bootable", "recovery", "gui")
    if not os.path.exists(gui_dir):
        print(f"Direktori GUI tidak ditemukan di: {gui_dir}")
        sys.exit(1)

    patched_count = 0
    for root, dirs, files in os.walk(gui_dir):
        for file in files:
            if file == "advanced.xml":
                file_path = os.path.join(root, file)
                if patch_advanced_xml(file_path):
                    patched_count += 1

    print(f"Total file advanced.xml yang disesuaikan: {patched_count}")

if __name__ == "__main__":
    main()
