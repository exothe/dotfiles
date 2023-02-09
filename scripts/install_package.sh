pm="None"

case "$( grep -Eoi 'Ubuntu|Arch' /etc/issue )" in
"Ubuntu")
    pm="apt"
    sudo apt update
    ;;
"Arch")
    pm="pacman"
    ;;
*)
    echo Your distribution is not supported by this install script!
    exit 1
    ;;
esac

function install_package {
    case $pm in
        "apt")
            sudo apt install $1
            ;;
        "pacman")
            sudo pacman -Syu $1
            ;;
    esac
}
