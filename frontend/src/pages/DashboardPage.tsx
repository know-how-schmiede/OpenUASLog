import { Alert, Card, CardContent, Skeleton, Typography } from '@mui/material'
import Grid from '@mui/material/Grid2'
import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { PageHeader } from '../components/PageHeader'
import type { Dashboard } from '../types'

export function DashboardPage() {
  const [data, setData] = useState<Dashboard | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api<Dashboard>('/reports/dashboard').then(setData).catch((reason) => setError(reason.message))
  }, [])

  const cards = [
    ['Flüge gesamt', data?.flights_total],
    ['Flüge diesen Monat', data?.flights_this_month],
    ['Gesamtflugzeit', data ? `${Math.floor(data.total_flight_minutes / 60)} h ${data.total_flight_minutes % 60} min` : null],
    ['Aktive Drohnen', data?.active_drones],
    ['Geplante Flüge', data?.planned_flights],
  ]

  return (
    <>
      <PageHeader title="Dashboard" />
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={3}>
        {cards.map(([label, value]) => (
          <Grid key={label} size={{ xs: 12, sm: 6, lg: 4 }}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>{label}</Typography>
                {value === null || value === undefined
                  ? <Skeleton width={100} height={48} />
                  : <Typography variant="h4">{value}</Typography>}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </>
  )
}
