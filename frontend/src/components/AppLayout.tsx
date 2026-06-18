import {
  Dashboard as DashboardIcon,
  Flight,
  Logout,
  PrecisionManufacturing,
  SettingsInputAntenna,
} from '@mui/icons-material'
import {
  AppBar,
  Box,
  Button,
  Divider,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const drawerWidth = 240

export function AppLayout() {
  const { user, logout } = useAuth()
  const items = [
    { label: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    { label: 'Flüge', path: '/flights', icon: <Flight /> },
    { label: 'Drohnen', path: '/drones', icon: <SettingsInputAntenna /> },
    ...(user?.role === 'admin'
      ? [{ label: 'Drohnen-Typen', path: '/drone-types', icon: <PrecisionManufacturing /> }]
      : []),
  ]

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'grey.50' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>OpenUASLog</Typography>
          <Typography variant="body2" sx={{ mr: 2 }}>
            {user?.full_name} · {user?.role}
          </Typography>
          <Button color="inherit" startIcon={<Logout />} onClick={logout}>Abmelden</Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <List>
          {items.map((item) => (
            <ListItemButton
              key={item.path}
              component={NavLink}
              to={item.path}
              end={item.path === '/'}
              sx={{ '&.active': { bgcolor: 'action.selected', color: 'primary.main' } }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
        <Divider />
        <Typography variant="caption" color="text.secondary" sx={{ p: 2 }}>
          Version 0.1.0
        </Typography>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  )
}
