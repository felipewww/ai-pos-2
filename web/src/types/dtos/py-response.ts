export type PyResponse = Array<{
  deliveryPoints: {
    lat: number,
    lng: number,
    is_priority: boolean,
  }[]
}>
