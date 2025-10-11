import {generateRandomString} from "@/utils/utils.ts";
import type {RouteCalc} from "@/types/route-calc.ts";

export class DeliveryPoint {
    private _isPriority: boolean = false;
    public id: string;

    private route: RouteCalc;

    constructor(
        public readonly address: string,
        public readonly lat: number,
        public readonly lng: number,
        private marker: google.maps.Marker,
    ) {
        this.id = generateRandomString();
    }

    get isPriority() {
        return this._isPriority;
    }

    setPriority(isPriority: boolean) {
        this._isPriority = isPriority;
    }

    removeMarker(): void {
        this.marker.setVisible(false);
        this.marker.setOpacity(0)
        this.marker.setMap(null);
    }

    showMarker(): void {
        this.marker.setVisible(true);
        this.marker.setOpacity(1)
    }

    assignRoute(route: RouteCalc) {
        console.log('\nassignRoute...........', route, this);
        this.route = route;
    }

    hasRoute(): boolean {
        return !!(this.route);
    }

    get routeProps() {
        return {
            id: this.route.id,
            color: this.route.color,
        }
    }
}
