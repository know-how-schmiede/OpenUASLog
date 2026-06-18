import { Add, Download } from '@mui/icons-material'
import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { FormEvent, useCallback, useEffect, useMemo, useState } from 'react'
import { api, downloadFlightsCsv } from '../api/client'
import { PageHeader } from '../components/PageHeader'
import { StatusChip } from '../components/StatusChip'
import type { Drone, Flight } from '../types'

export function FlightsPage() {
  const [rows, setRows] = useState<Flight[]>([])
  const [drones, setDrones] = useState<Drone[]>([])
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    drone_id: '',
    date: new Date().toISOString().slice(0, 10),
    start_time: '',
    end_time: '',
    location_name: '',
    flight_type: 'Training',
    status: 'completed',
    purpose: '',
  })

  const load = useCallback(() => {
    Promise.all([api<Flight[]>('/flights'), api<Drone[]>('/drones')])
      .then(([flights, availableDrones]) => {
        setRows(flights)
        setDrones(availableDrones)
      })
      .catch((reason) => setError(reason.message))
  }, [])

  useEffect(load, [load])

  const droneNames = useMemo(
    () => Object.fromEntries(drones.map((drone) => [drone.id, drone.name])),
    [drones],
  )
  const columns: GridColDef<Flight>[] = [
    { field: 'date', headerName: 'Datum', width: 120 },
    { field: 'start_time', headerName: 'Start', width: 100 },
    { field: 'duration_minutes', headerName: 'Dauer (min)', type: 'number', width: 120 },
    { field: 'drone_id', headerName: 'Drohne', flex: 1, valueFormatter: (value: number) => droneNames[value] ?? value },
    { field: 'location_name', headerName: 'Ort', flex: 1 },
    { field: 'flight_type', headerName: 'Flugart', flex: 1 },
    { field: 'status', headerName: 'Status', width: 140, renderCell: ({ value }) => <StatusChip value={value} /> },
  ]

  async function submit(event: FormEvent) {
    event.preventDefault()
    try {
      await api('/flights', {
        method: 'POST',
        body: JSON.stringify({
          ...form,
          drone_id: Number(form.drone_id),
          end_time: form.end_time || null,
          purpose: form.purpose || null,
        }),
      })
      setOpen(false)
      load()
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Speichern fehlgeschlagen.')
    }
  }

  return (
    <>
      <PageHeader
        title="Flüge"
        action={
          <Stack direction="row" spacing={1}>
            <Button startIcon={<Download />} onClick={() => downloadFlightsCsv().catch((reason) => setError(reason.message))}>
              CSV
            </Button>
            <Button variant="contained" startIcon={<Add />} onClick={() => setOpen(true)}>Neuer Flug</Button>
          </Stack>
        }
      />
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <DataGrid rows={rows} columns={columns} autoHeight disableRowSelectionOnClick />
      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <form onSubmit={submit}>
          <DialogTitle>Flug dokumentieren</DialogTitle>
          <DialogContent>
            <Stack spacing={2} sx={{ mt: 1 }}>
              <TextField select label="Drohne" value={form.drone_id} onChange={(event) => setForm({ ...form, drone_id: event.target.value })} required>
                {drones.map((drone) => <MenuItem key={drone.id} value={drone.id}>{drone.name}</MenuItem>)}
              </TextField>
              <TextField type="date" label="Datum" value={form.date} onChange={(event) => setForm({ ...form, date: event.target.value })} slotProps={{ inputLabel: { shrink: true } }} required />
              <Stack direction="row" spacing={2}>
                <TextField type="time" label="Startzeit" value={form.start_time} onChange={(event) => setForm({ ...form, start_time: event.target.value })} slotProps={{ inputLabel: { shrink: true } }} required fullWidth />
                <TextField type="time" label="Endzeit" value={form.end_time} onChange={(event) => setForm({ ...form, end_time: event.target.value })} slotProps={{ inputLabel: { shrink: true } }} fullWidth />
              </Stack>
              <TextField label="Ort" value={form.location_name} onChange={(event) => setForm({ ...form, location_name: event.target.value })} required />
              <TextField label="Flugart" value={form.flight_type} onChange={(event) => setForm({ ...form, flight_type: event.target.value })} required />
              <TextField select label="Status" value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })}>
                <MenuItem value="planned">geplant</MenuItem>
                <MenuItem value="completed">durchgeführt</MenuItem>
                <MenuItem value="cancelled">storniert</MenuItem>
                <MenuItem value="aborted">abgebrochen</MenuItem>
              </TextField>
              <TextField label="Zweck" value={form.purpose} onChange={(event) => setForm({ ...form, purpose: event.target.value })} multiline rows={2} />
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpen(false)}>Abbrechen</Button>
            <Button type="submit" variant="contained">Speichern</Button>
          </DialogActions>
        </form>
      </Dialog>
    </>
  )
}
