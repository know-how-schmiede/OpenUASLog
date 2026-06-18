import { CircularProgress, CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './auth/AuthContext'
import { AppLayout } from './components/AppLayout'
import { DashboardPage } from './pages/DashboardPage'
import { DronesPage } from './pages/DronesPage'
import { DroneTypesPage } from './pages/DroneTypesPage'
import { FlightsPage } from './pages/FlightsPage'
import { LoginPage } from './pages/LoginPage'

const theme = createTheme({
  palette: {
    primary: { main: '#0b4f6c' },
    secondary: { main: '#f28f3b' },
  },
  shape: { borderRadius: 10 },
})

export default function App() {
  const { user, loading } = useAuth()
  if (loading) return <CircularProgress sx={{ position: 'fixed', top: '50%', left: '50%' }} />

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        {!user ? (
          <Routes>
            <Route path="*" element={<LoginPage />} />
          </Routes>
        ) : (
          <Routes>
            <Route element={<AppLayout />}>
              <Route index element={<DashboardPage />} />
              <Route path="flights" element={<FlightsPage />} />
              <Route path="drones" element={<DronesPage />} />
              <Route
                path="drone-types"
                element={user.role === 'admin' ? <DroneTypesPage /> : <Navigate to="/" replace />}
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        )}
      </BrowserRouter>
    </ThemeProvider>
  )
}
