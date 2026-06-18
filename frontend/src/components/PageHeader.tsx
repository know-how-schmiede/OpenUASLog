import { Box, Typography } from '@mui/material'

export function PageHeader({
  title,
  action,
}: {
  title: string
  action?: React.ReactNode
}) {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
      <Typography variant="h4">{title}</Typography>
      {action}
    </Box>
  )
}
