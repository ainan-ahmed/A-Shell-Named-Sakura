project('gtk-app-launcher',
  version: '0.1.0',
  meson_version: '>= 0.59.0',
)

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
bindir = get_option('prefix') / get_option('bindir')

blp = find_program('blueprint-compiler', required: true)

# Try to find python in venv first, then fall back to system python
venv_python = meson.project_source_root() / '.venv' / 'bin' / 'python'
if run_command(venv_python, '-c', 'import sass', check: false).returncode() == 0
  python = find_program(venv_python)
else
  python = find_program('python3', required: true)
endif

layer_shell = dependency('gtk4-layer-shell-0')

blueprint_sources = files(
  'src/ui/launcher.blp',
  'src/ui/app_row.blp',
)

# Compile blueprints
ui = custom_target(
  'blueprint',
  input: blueprint_sources,
  output: '.',
  command: [
    blp,
    'batch-compile',
    '@OUTPUT@',
    '@CURRENT_SOURCE_DIR@/src/ui',
    '@INPUT@',
  ],
)

# Compile SCSS to CSS using libsass
css = custom_target(
  'scss',
  input: files('src/style.scss'),
  output: 'style.css',
  command: [python, files('build_scripts/compile_scss.py'), '@INPUT@', '@OUTPUT@'],
)

# Compile UI and CSS into a binary GResource
import('gnome').compile_resources(
  'data',
  files('src/app.gresource.xml'),
  dependencies: [ui, css],
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# Install Python sources and packages
install_data(
  'src/__init__.py',
  'src/main.py',
  install_dir: pkgdatadir,
)

install_data(
  'src/services/__init__.py',
  'src/services/apps_service.py',
  install_dir: pkgdatadir / 'services',
)

install_data(
  'src/windows/__init__.py',
  'src/windows/launcher.py',
  install_dir: pkgdatadir / 'windows',
)

install_data(
  'src/widgets/__init__.py',
  'src/widgets/app_row.py',
  install_dir: pkgdatadir / 'widgets',
)

install_data(
  'src/utils/__init__.py',
  'src/utils/resource_loader.py',
  install_dir: pkgdatadir / 'utils',
)

# Install desktop file
install_data(
  'data/com.launcher.app.desktop',
  install_dir: get_option('datadir') / 'applications',
)

# Create executable wrapper script that calls main.py
configure_file(
  input: 'gtk-app-launcher.in',
  output: meson.project_name(),
  configuration: {
    'PYTHON': python.full_path(),
    'PKGDATADIR': pkgdatadir,
  },
  install: true,
  install_dir: bindir,
)
