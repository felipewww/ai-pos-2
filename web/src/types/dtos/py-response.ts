export type PyResponse = {
    routes: {
        deliveryPoints: {
            id: string
            lat: number
            lng: number
            is_priority: boolean
        }[]
    }[]

    // best_route: {
    //     id: string
    //     lat: number
    //     lng: number
    //     is_priority: boolean
    // }[]
    //
    // best_distance: number
    //
    // fit_history: number[]

    conversation: string,
}
