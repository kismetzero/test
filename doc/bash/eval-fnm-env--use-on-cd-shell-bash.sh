export PATH="/run/user/1001/fnm_multishells/256294_1781079080100/bin":"$PATH"
export FNM_MULTISHELL_PATH="/run/user/1001/fnm_multishells/256294_1781079080100"
export FNM_VERSION_FILE_STRATEGY="local"
export FNM_DIR="/home/dev/.local/share/fnm"
export FNM_LOGLEVEL="info"
export FNM_NODE_DIST_MIRROR="https://nodejs.org/dist"
export FNM_COREPACK_ENABLED="false"
export FNM_RESOLVE_ENGINES="true"
export FNM_ARCH="x64"
__fnm_use_if_file_found() {
    if [[ -f .node-version || -f .nvmrc || -f package.json ]]; then
    fnm use --silent-if-unchanged
fi

}

__fnmcd() {
    \cd "$@" || return $?
    __fnm_use_if_file_found
}

alias cd=__fnmcd

