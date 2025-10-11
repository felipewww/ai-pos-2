export type PyResponse = Array<{
    deliveryPoints: {
        id: string;
        lat: number,
        lng: number,
        is_priority: boolean,
    }[]
}>
