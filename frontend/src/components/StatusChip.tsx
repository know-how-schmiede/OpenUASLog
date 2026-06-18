import { Chip } from '@mui/material'

export function StatusChip({ value }: { value: string }) {
  const color =
    value === 'active' || value === 'completed'
      ? 'success'
      : value === 'planned'
        ? 'info'
        : value === 'maintenance' || value === 'cancelled'
          ? 'warning'
          : 'default'
  return <Chip label={value} color={color} size="small" />
}
