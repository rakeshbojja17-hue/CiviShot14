[app]
title = CiviShot
package.name = civishot
package.domain = com.civishot.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 0

android.permissions = CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1

