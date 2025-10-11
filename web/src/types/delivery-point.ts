export class DeliveryPoint {
    private _isPriority: boolean = false;

    constructor(
        public readonly address: string,
        public readonly lat: number,
        public readonly lng: number,
        private marker: google.maps.Marker,
        // public readonly isPriority: boolean,
    ) {
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
}
