import { Add } from '@mui/icons-material'
import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Stack,
  TextField,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { FormEvent, useCallback, useEffect, useState } from 'react'
import { api } from '../api/client'
import { PageHeader } from '../components/PageHeader'
import type { DroneType } from '../types'

const columns: GridColDef<DroneType>[] = [
  { field: 'manufacturer', headerName: 'Hersteller', flex: 1 },
  { field: 'model', headerName: 'Modell', flex: 1 },
  { field: 'variant', headerName: 'Variante', flex: 1 },
  { field: 'category', headerName: 'Kategorie', flex: 1 },
  { field: 'drone_class', headerName: 'Klasse', width: 100 },
  { field: 'weight_g', headerName: 'Gewicht (g)', type: 'number', width: 130 },
  { field: 'max_flight_time_min', headerName: 'Flugzeit (min)', type: 'number', width: 140 },
  { field: 'is_active', headerName: 'Aktiv', type: 'boolean', width: 90 },
]

export function DroneTypesPage() {
  const [rows, setRows] = useState<DroneType[]>([])
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    manufacturer: '',
    model: '',
    variant: '',
    category: '',
    drone_class: '',
    weight_g: '',
    max_flight_time_min: '',
  })

  const load = useCallback(() => {
    api<DroneType[]>('/drone-types').then(setRows).catch((reason) => setError(reason.message))
  }, [])

  useEffect(load, [load])

  async function submit(event: FormEvent) {
    event.preventDefault()
    setError('')
    try {
      await api('/drone-types', {
        method: 'POST',
        body: JSON.stringify({
          ...form,
          variant: form.variant || null,
          category: form.category || null,
          drone_class: form.drone_class || null,
          weight_g: form.weight_g ? Number(form.weight_g) : null,
          max_flight_time_min: form.max_flight_time_min ? Number(form.max_flight_time_min) : null,
        }),
      })
      setOpen(false)
      setForm({ manufacturer: '', model: '', variant: '', category: '', drone_class: '', weight_g: '', max_flight_time_min: '' })
      load()
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Speichern fehlgeschlagen.')
    }
  }

  return (
    <>
      <PageHeader
        title="Drohnen-Typen"
        action={<Button variant="contained" startIcon={<Add />} onClick={() => setOpen(true)}>Neuer Typ</Button>}
      />
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <DataGrid rows={rows} columns={columns} autoHeight disableRowSelectionOnClick />
      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <BoxForm title="Drohnen-Typ anlegen" onSubmit={submit}>
          {Object.entries(form).map(([key, value]) => (
            <TextField
              key={key}
              label={{
                manufacturer: 'Hersteller',
                model: 'Modell',
                variant: 'Variante',
                category: 'Kategorie',
                drone_class: 'Drohnenklasse',
                weight_g: 'Gewicht (g)',
                max_flight_time_min: 'Max. Flugzeit (min)',
              }[key]}
              type={key.includes('weight') || key.includes('time') ? 'number' : 'text'}
              value={value}
              onChange={(event) => setForm({ ...form, [key]: event.target.value })}
              required={key === 'manufacturer' || key === 'model'}
              fullWidth
            />
          ))}
        </BoxForm>
      </Dialog>
    </>
  )
}

function BoxForm({
  title,
  onSubmit,
  children,
}: {
  title: string
  onSubmit: (event: FormEvent) => void
  children: React.ReactNode
}) {
  return (
    <form onSubmit={onSubmit}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>{children}</Stack>
      </DialogContent>
      <DialogActions>
        <Button type="submit" variant="contained">Speichern</Button>
      </DialogActions>
    </form>
  )
}
