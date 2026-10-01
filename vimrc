set nocompatible

set nobackup
set nowritebackup
set noswapfile
set viminfo=

syntax on

"set autoindent

colorscheme slate

" Line Numbers
set number
"highlight LineNr term=NONE cterm=NONE ctermfg=White ctermbg=Black

" Right border
"set colorcolumn=80

" Ignore case for searches
set ignorecase

" Unless you type an uppercase letter
set smartcase

" Highlight things that we find with the search
set hlsearch

" Tabs
set smarttab
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4

" Autohandle file types
filetype on
filetype plugin on
filetype indent on

" Max highlight
let python_highlight_all = 1

" 256 colors (X only)
set t_Co=256

" Omnicompletion
autocmd FileType python     set omnifunc=python3complete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html       set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css        set omnifunc=csscomplete#CompleteCSS

" Autocomplete sources
set complete=.,k,b,t

" *.py: Trim trailing spaces on save, keeping the cursor in place
function! TrimTrailingSpaces()
    let l:view = winsaveview()
    %s/\s\+$//e
    call winrestview(l:view)
endfunction
autocmd BufWritePre *.py call TrimTrailingSpaces()
