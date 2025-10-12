export type PyResponse = {
  routes: {
    deliveryPoints: {
      id: string;
      lat: number;
      lng: number;
      is_priority: boolean;
    }[];
    info: {
      population_size: number;
      fit_history: {
        generation: number;
        best: number;
        mean: number;
        worst: number;
      }[];
    };
  }[];

  // best_route: {
  //   id: string
  //   lat: number
  //   lng: number
  //   is_priority: boolean
  // }[]

  // best_distance: number

  // fit_history: number[]
};
