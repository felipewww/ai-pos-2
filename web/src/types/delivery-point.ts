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
}
