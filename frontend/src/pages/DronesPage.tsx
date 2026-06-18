import { Add } from '@mui/icons-material'
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
import { api } from '../api/client'
import { PageHeader } from '../components/PageHeader'
import { StatusChip } from '../components/StatusChip'
import type { Drone, DroneType } from '../types'

export function DronesPage() {
  const [rows, setRows] = useState<Drone[]>([])
  const [types, setTypes] = useState<DroneType[]>([])
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    drone_type_id: '',
    name: '',
    serial_number: '',
    registration_mark: '',
    firmware_version: '',
  })

  const load = useCallback(() => {
    Promise.all([
      api<Drone[]>('/drones'),
      api<DroneType[]>('/drone-types?active_only=true'),
    ])
      .then(([drones, droneTypes]) => {
        setRows(drones)
        setTypes(droneTypes)
      })
      .catch((reason) => setError(reason.message))
  }, [])

  useEffect(load, [load])

  const typeNames = useMemo(
    () => Object.fromEntries(types.map((type) => [type.id, `${type.manufacturer} ${type.model}`])),
    [types],
  )
  const columns: GridColDef<Drone>[] = [
    { field: 'name', headerName: 'Name', flex: 1 },
    {
      field: 'drone_type_id',
      headerName: 'Drohnen-Typ',
      flex: 1,
      valueFormatter: (value: number) => typeNames[value] ?? value,
    },
    { field: 'serial_number', headerName: 'Seriennummer', flex: 1 },
    { field: 'registration_mark', headerName: 'Kennzeichen', flex: 1 },
    { field: 'firmware_version', headerName: 'Firmware', flex: 1 },
    { field: 'status', headerName: 'Status', width: 130, renderCell: ({ value }) => <StatusChip value={value} /> },
  ]

  async function submit(event: FormEvent) {
    event.preventDefault()
    try {
      await api('/drones/from-template', {
        method: 'POST',
        body: JSON.stringify({
          ...form,
          drone_type_id: Number(form.drone_type_id),
          serial_number: form.serial_number || null,
          registration_mark: form.registration_mark || null,
          firmware_version: form.firmware_version || null,
        }),
      })
      setOpen(false)
      setForm({ drone_type_id: '', name: '', serial_number: '', registration_mark: '', firmware_version: '' })
      load()
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Speichern fehlgeschlagen.')
    }
  }

  return (
    <>
      <PageHeader
        title="Drohnen"
        action={<Button variant="contained" startIcon={<Add />} onClick={() => setOpen(true)}>Neue Drohne</Button>}
      />
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <DataGrid rows={rows} columns={columns} autoHeight disableRowSelectionOnClick />
      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <form onSubmit={submit}>
          <DialogTitle>Drohne aus Vorlage anlegen</DialogTitle>
          <DialogContent>
            <Stack spacing={2} sx={{ mt: 1 }}>
              <TextField
                select
                label="Drohnen-Typ"
                value={form.drone_type_id}
                onChange={(event) => setForm({ ...form, drone_type_id: event.target.value })}
                required
              >
                {types.map((type) => (
                  <MenuItem key={type.id} value={type.id}>
                    {type.manufacturer} {type.model} {type.variant}
                  </MenuItem>
                ))}
              </TextField>
              <TextField label="Name" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
              <TextField label="Seriennummer" value={form.serial_number} onChange={(event) => setForm({ ...form, serial_number: event.target.value })} />
              <TextField label="Kennzeichen" value={form.registration_mark} onChange={(event) => setForm({ ...form, registration_mark: event.target.value })} />
              <TextField label="Firmware-Version" value={form.firmware_version} onChange={(event) => setForm({ ...form, firmware_version: event.target.value })} />
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
