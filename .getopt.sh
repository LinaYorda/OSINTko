# Supported options are (from build.sh):
# -d | --distribution <distro>
# -p | --proposed-updates
# -a | --arch <architecture>
# -v | --verbose
# -D | --debug
# -s | --salt
# -h | --help
#      --installer
#      --live
#      --variant <variant>
#      --version <version>
#      --subdir <directory-name>
#      --get-image-path
#      --no-clean
#      --clean

BUILD_OPTS_SHORT="d:pa:vDsh"
BUILD_OPTS_LONG="distribution:,proposed-updates,arch:,verbose,debug,salt,installer,live,variant:,version:,subdir:,get-image-path,no-clean,clean,help"
