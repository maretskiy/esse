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

" Max highlight
let python_highlight_all = 1

" 256 colors (X only)
set t_Co=256

" Omnicomletion
autocmd FileType python     set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html       set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css        set omnifunc=csscomplete#CompleteCSSi

" Autocomplete by Tab
function InsertTabWrapper()
    let col = col('.') - 1
        if !col || getline('.')[col - 1] !~ '\k'
        return "\"
    else
        return "\<c-p>"
    endif
endfunction

" Show autocomplete options
"imap <c-r>=InsertTabWrapper()
set complete=""
set complete+=.
set complete+=k
set complete+=b
set complete+=t

" *.py: Trim trailing spaces on save
autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``

" *.py: Use smart indentation after keywords
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
