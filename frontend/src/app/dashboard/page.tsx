'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import {
  Search,
  LogOut,
  Settings,
  Terminal,
  Layers,
  Command as CommandIcon,
  Plus,
  X,
  GripHorizontal,
  ChevronDown
} from 'lucide-react'

interface SearchResult {
  id: string
  title: string
  description?: string
  category?: string
}

interface TerminalTab {
  id: string
  title: string
  content: string[]
  currentInput: string
}

export default function HomePage() {
  const router = useRouter()
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [activeSection, setActiveSection] = useState<'cluster' | 'terminal' | 'settings'>('cluster')

  // Terminal states
  const [terminalVisible, setTerminalVisible] = useState(false)
  const [terminalHeight, setTerminalHeight] = useState(300)
  const [isResizing, setIsResizing] = useState(false)
  const [terminalTabs, setTerminalTabs] = useState<TerminalTab[]>([
    { id: '1', title: 'Terminal 1', content: ['$ Welcome to AI Terminal'], currentInput: '' },
  ])
  const [activeTabId, setActiveTabId] = useState('1')

  const searchInputRef = useRef<HTMLInputElement>(null)
  const terminalInputRef = useRef<HTMLInputElement>(null)
  const resizeRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        setSearchOpen(true)
        setTimeout(() => searchInputRef.current?.focus(), 100)
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === '`' || e.key === '~')) {
        e.preventDefault()
        setTerminalVisible((v) => !v)
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [])

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return
      const newHeight = window.innerHeight - e.clientY
      setTerminalHeight(Math.max(150, Math.min(600, newHeight)))
    }
    const handleMouseUp = () => setIsResizing(false)
    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
    }
    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isResizing])

  const performSearch = async (query: string) => {
    if (!query.trim()) {
      setSearchResults([])
      return
    }
    const commonResults: SearchResult[] = [
      { id: 'help', title: 'Help Center', description: 'Get assistance and FAQs', category: 'General' },
      { id: 'logout', title: 'Logout', description: 'Sign out of your account', category: 'Account' },
    ]
    const clusterResults: SearchResult[] = [
      { id: 'cluster-config', title: 'Configure Cluster', description: 'Adjust cluster settings', category: 'Cluster' },
      { id: 'cluster-nodes', title: 'View Cluster Nodes', description: 'List all nodes', category: 'Cluster' },
      { id: 'cluster-logs', title: 'Cluster Logs', description: 'Monitor cluster logs', category: 'Cluster' },
    ]
    const settingsResults: SearchResult[] = [
      { id: 'profile', title: 'Update Profile', description: 'Edit your user profile', category: 'Settings' },
      { id: 'notifications', title: 'Notification Settings', description: 'Manage notification preferences', category: 'Settings' },
    ]
    let results: SearchResult[] = []
    if (activeSection === 'cluster') {
      results = [...clusterResults, ...commonResults]
    } else if (activeSection === 'settings') {
      results = [...settingsResults, ...commonResults]
    } else {
      results = [...clusterResults, ...settingsResults, ...commonResults]
    }
    const filtered = results.filter(
      (item) =>
        item.title.toLowerCase().includes(query.toLowerCase()) ||
        item.description?.toLowerCase().includes(query.toLowerCase())
    )
    setSearchResults(filtered)
  }

  const handleLogout = async () => {
    try {
      await fetch('/next-api/logout', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
      })
      router.push('/login')
    } catch (err) {
      console.error(err)
      alert('Logout failed. Please try again.')
    }
  }

  const handleSearchSelect = (result: SearchResult) => {
    setSearchOpen(false)
    setSearchQuery('')
    if (result.id === 'ui-colors') {
      setActiveSection('settings')
      setTimeout(() => {
        document.getElementById('sidebar-color-settings')?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    }
    console.log('Search selected:', result)
  }

  const addNewTab = () => {
    const newId = Date.now().toString()
    const newTab: TerminalTab = {
      id: newId,
      title: `Terminal ${terminalTabs.length + 1}`,
      content: ['$ Welcome to AI Terminal'],
      currentInput: '',
    }
    setTerminalTabs((prev) => [...prev, newTab])
    setActiveTabId(newId)
  }

  const closeTab = (tabId: string) => {
    if (terminalTabs.length === 1) return
    setTerminalTabs((prev) => prev.filter((tab) => tab.id !== tabId))
    if (activeTabId === tabId) {
      const remaining = terminalTabs.filter((tab) => tab.id !== tabId)
      setActiveTabId(remaining[0]?.id ?? '')
    }
  }

  const handleTerminalInput = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const activeTab = terminalTabs.find((tab) => tab.id === activeTabId)
      if (!activeTab) return
      const input = activeTab.currentInput
      const newContent = [...activeTab.content, `$ ${input}`]
      switch (input.trim()) {
        case 'clear':
          newContent.splice(0, newContent.length - 1)
          break
        case 'help':
          newContent.push('Available commands: help, clear, ls, pwd, whoami')
          break
        case 'ls':
          newContent.push('file1.txt  file2.js  directory1/  directory2/')
          break
        case 'pwd':
          newContent.push('/home/user/workspace')
          break
        case 'whoami':
          newContent.push('ai-user')
          break
        default:
          newContent.push(`Command not found: ${input}`)
          break
      }
      setTerminalTabs((prev) =>
        prev.map((tab) =>
          tab.id === activeTabId ? { ...tab, content: newContent, currentInput: '' } : tab
        )
      )
    }
  }

  const updateCurrentInput = (value: string) => {
    setTerminalTabs((prev) =>
      prev.map((tab) => (tab.id === activeTabId ? { ...tab, currentInput: value } : tab))
    )
  }

  const activeTab = terminalTabs.find((tab) => tab.id === activeTabId)

  const sidebarItems = [
    {
      id: 'cluster' as const,
      label: 'Cluster Select',
      icon: Layers,
    },
    {
      id: 'terminal' as const,
      label: 'AI Terminal',
      icon: Terminal,
    },
    {
      id: 'settings' as const,
      label: 'Settings',
      icon: Settings,
    },
  ]

  const handleSidebarClick = (id: 'cluster' | 'terminal' | 'settings') => {
    if (id === 'terminal') {
      setTerminalVisible((v) => !v)
    } else {
      setActiveSection(id)
      setTerminalVisible(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-background font-sans text-foreground selection:bg-primary selection:text-primary-foreground">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 rounded-tl-lg rounded-tr-lg shadow-sm">
        <div className="flex h-12 items-center justify-between px-4">
          <div className="flex-1 rounded-l-lg"></div>

          {/* Wider search bar */}
          <div className="flex-1 max-w-xl mx-4 rounded-lg">
            <Popover open={searchOpen} onOpenChange={setSearchOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  role="combobox"
                  aria-expanded={searchOpen}
                  className="w-full justify-between text-muted-foreground rounded-lg"
                >
                  <div className="flex items-center gap-2">
                    <Search className="h-4 w-4" />
                    <span className="text-sm">Search...</span>
                  </div>
                  <div className="flex items-center gap-1 text-xs">
                    <CommandIcon className="h-3 w-3" />
                    <span>K</span>
                  </div>
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-[500px] p-0 rounded-lg" align="center">
                <Command>
                  <CommandInput
                    ref={searchInputRef}
                    placeholder="Type to search..."
                    value={searchQuery}
                    onValueChange={(value) => {
                      setSearchQuery(value)
                      performSearch(value)
                    }}
                    className="rounded-t-lg border-b border-border"
                  />
                  <CommandList className="max-h-[300px] overflow-y-auto rounded-b-lg">
                    <CommandEmpty>No results found.</CommandEmpty>
                    {searchResults.length > 0 && (
                      <CommandGroup heading="Results">
                        {searchResults.map((result) => (
                          <CommandItem
                            key={result.id}
                            value={result.title}
                            onSelect={() => handleSearchSelect(result)}
                            className="cursor-pointer"
                          >
                            <div className="flex flex-col gap-1">
                              <span className="font-medium">{result.title}</span>
                              {result.description && (
                                <span className="text-sm text-muted-foreground">{result.description}</span>
                              )}
                            </div>
                          </CommandItem>
                        ))}
                      </CommandGroup>
                    )}
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>
          </div>

          <div className="flex-1 flex justify-end rounded-r-lg">
            <Button
              type="button"
              onClick={handleLogout}
              variant="outline"
              size="sm"
              className="rounded-lg"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden relative">
        {/* Sidebar */}
        <aside
          className="flex flex-col items-center w-16 min-h-full border-r border-border rounded-bl-lg rounded-tl-lg shadow-[inset_1px_0_0_#d1d5db] z-20"
          style={{ userSelect: 'none' }}
        >
          <nav className="flex flex-col items-center py-4 space-y-6 flex-1">
            {sidebarItems.map(({ id, label, icon: Icon }) => (
              <Button
                key={id}
                variant={activeSection === id ? 'default' : 'ghost'}
                size="sm"
                className={cn(
                  'w-12 h-12 p-0 rounded-xl transition-colors',
                  activeSection === id
                    ? 'bg-black text-white' // Active button: black background and black text
                    : 'text-muted-foreground hover:text-foreground hover:bg-accent' // Inactive button styles remain
                )}
                onClick={() => handleSidebarClick(id)}
                title={label}
                aria-pressed={activeSection === id}
              >
                <Icon className="h-6 w-6" />
              </Button>
            ))}
          </nav>
        </aside>

        {/* Main content */}
        <main className="flex-1 p-6 overflow-auto rounded-tr-lg rounded-br-lg">
          <div className="max-w-4xl mx-auto rounded-lg">
            {activeSection === 'cluster' && (
              <div className="space-y-6 rounded-lg border border-border bg-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Layers className="h-6 w-6" />
                  <h1 className="text-2xl font-bold">Cluster Select</h1>
                </div>
                <p className="text-muted-foreground">Configure and manage your clusters here.</p>
              </div>
            )}

            {activeSection === 'settings' && (
              <div className="space-y-6 rounded-lg border border-border bg-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Settings className="h-6 w-6" />
                  <h1 className="text-2xl font-bold">Settings</h1>
                </div>
              </div>
            )}
          </div>
        </main>

        {/* Terminal overlay */}
        {terminalVisible && (
          <div
            className={cn(
              'absolute bottom-0 left-16 right-0 z-10',
              'border-t border-border bg-card',
              'flex flex-col rounded-t-lg shadow-lg shadow-black/20',
              'transition-transform duration-300 ease-in-out'
            )}
            style={{ height: terminalHeight, minHeight: 150, maxHeight: 600 }}
          >
            {/* Resize handle */}
            <div
              ref={resizeRef}
              className="h-2 cursor-row-resize flex items-center justify-center bg-border hover:bg-primary rounded-t-lg select-none"
              onMouseDown={() => setIsResizing(true)}
              aria-label="Resize terminal panel"
              role="slider"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'ArrowUp') {
                  e.preventDefault()
                  setTerminalHeight((h) => Math.min(600, h + 10))
                } else if (e.key === 'ArrowDown') {
                  e.preventDefault()
                  setTerminalHeight((h) => Math.max(150, h - 10))
                }
              }}
            >
              <GripHorizontal className="h-4 w-4 text-muted-foreground" />
            </div>

            {/* Terminal Tabs */}
            <div className="flex items-center justify-between border-b border-border bg-muted/30 px-2 select-none">
              <div className="flex space-x-1 overflow-x-auto">
                {terminalTabs.map((tab) => (
                  <div
                    key={tab.id}
                    className={cn(
                      'flex items-center gap-1 px-4 py-2 text-sm border-r border-border cursor-pointer whitespace-nowrap select-none',
                      activeTabId === tab.id
                        ? 'bg-background text-foreground font-semibold'
                        : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                    )}
                    onClick={() => setActiveTabId(tab.id)}
                    role="tab"
                    aria-selected={activeTabId === tab.id}
                    tabIndex={activeTabId === tab.id ? 0 : -1}
                  >
                    <Terminal className="h-4 w-4" />
                    <span>{tab.title}</span>
                    {terminalTabs.length > 1 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-5 w-5 p-0 hover:bg-destructive hover:text-destructive-foreground focus:outline-none"
                        onClick={(e) => {
                          e.stopPropagation()
                          closeTab(tab.id)
                        }}
                        aria-label={`Close ${tab.title}`}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={addNewTab}
                  className="m-1 h-6 w-6 p-0 flex items-center justify-center"
                  aria-label="Add new terminal tab"
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>

              {/* Hide terminal button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setTerminalVisible(false)}
                aria-label="Hide Terminal"
                className="mx-2"
              >
                <ChevronDown className="h-6 w-6" />
              </Button>
            </div>

            {/* Terminal Content */}
            <div
              className="flex-1 p-4 font-mono text-sm bg-black text-green-400 overflow-y-auto rounded-b-lg"
              tabIndex={0}
            >
              {activeTab && (
                <div className="space-y-1">
                  {activeTab.content.map((line, index) => (
                    <div key={index}>{line}</div>
                  ))}
                  <div className="flex items-center">
                    <span className="text-green-400 select-none">$ </span>
                    <Input
                      ref={terminalInputRef}
                      value={activeTab.currentInput}
                      onChange={(e) => updateCurrentInput(e.target.value)}
                      onKeyDown={handleTerminalInput}
                      className="border-none bg-transparent text-green-400 p-0 h-auto focus:ring-0 focus:border-none font-mono flex-1"
                      spellCheck={false}
                      autoComplete="off"
                      autoCorrect="off"
                      autoCapitalize="off"
                      placeholder=""
                      aria-label="Terminal command input"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}