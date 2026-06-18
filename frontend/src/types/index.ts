export type Role = 'admin' | 'pilot'

export interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: Role
  is_active: boolean
}

export interface DroneType {
  id: number
  manufacturer: string
  model: string
  variant: string | null
  category: string | null
  drone_class: string | null
  weight_g: number | null
  max_flight_time_min: number | null
  max_speed_kmh: number | null
  battery_type: string | null
  is_active: boolean
}

export interface Drone {
  id: number
  owner_user_id: number
  drone_type_id: number
  name: string
  serial_number: string | null
  registration_mark: string | null
  firmware_version: string | null
  status: string
}

export interface Flight {
  id: number
  drone_id: number
  pilot_user_id: number
  date: string
  start_time: string
  end_time: string | null
  duration_minutes: number
  location_name: string
  flight_type: string
  status: string
}

export interface Dashboard {
  flights_total: number
  flights_this_month: number
  total_flight_minutes: number
  active_drones: number
  planned_flights: number
}
