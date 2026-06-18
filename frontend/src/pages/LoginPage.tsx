import { Alert, Box, Button, Card, CardContent, TextField, Typography } from '@mui/material'
import { FormEvent, useState } from 'react'
import { useAuth } from '../auth/AuthContext'

export function LoginPage() {
  const { login } = useAuth()
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login(username, password)
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Anmeldung fehlgeschlagen.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center', bgcolor: 'grey.100', p: 2 }}>
      <Card sx={{ width: '100%', maxWidth: 420 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>OpenUASLog</Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>
            Anmeldung am UAS-Flugbuch
          </Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              label="Benutzername oder E-Mail"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              margin="normal"
              fullWidth
              required
            />
            <TextField
              label="Passwort"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              margin="normal"
              fullWidth
              required
            />
            <Button type="submit" variant="contained" size="large" fullWidth disabled={submitting} sx={{ mt: 2 }}>
              Anmelden
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  )
}
