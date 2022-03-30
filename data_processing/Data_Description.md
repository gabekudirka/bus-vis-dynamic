# Description of Generated Data Files

## Buses

#### p20.json, p60.json, p80.json

Bus objects for each of the conversion plans

STRUCTURE:
buses: array of bus objects {
    id: string
    stops: array of stop objects {
        stop_id: int
        stop_name: string
        arrival_time: string
        departure_time: string
        direction: string
        distance_traveled: float
        remaining_charge: float
        is_charging: bool
    }
}

## Plans

#### p20.json, p60.json, p80.json

Plan information for each of the conversion plans

STRUCTURE:
Object {
    plan_name: string
    charging_stations: array of charging station objects {
        stop_id: string
        stop_name: string
        num_stations: int
    }
    env_equity: float
    converted_buses: array of bus id's (strings)
    num_buses: int
    num_miles: float
    num_charging_stations: int
}

## StationLocations

#### p20.json, p60.json, p80.json

Location information for all stations in each of the conversion plans

STRUCTURE:
GeoJson Object{
    type: string (featureCollection)
    features: array of feature objects {
        type: string (Feature)
        geometry: object {
            type: string (Point)
            coordinates: array of floats (size 2)
        }
        properties: object {
            stop_id: string
            stop_name: string
            num_stations: int
        }
    }
}

## Supplementary

#### pollutant_concentration.json

Shape & properties file for pollutant info

STRUCTURE:
Features {
    features: array of objects: {
        geometry: obect {
            type: string (Point)
            coordinates: coordinate array of X, Y (size 2, floats)
        }
        properties:
            PM25: string
        type: string (Feature)
    }

#### taz_region_data.json

Shape & properties file for TAZ region info

STRUCTURE:
Feature Collection object {
    type: string
    features: array of objects {
        type: string
        geometry: obect {
            type: string (polygon)
            coordinates: array of coordinate pairs
        }
        properties:
            N___CO_TAZ: int
            AREA: float
            inc_bracket1: float
            inc_bracket2: float
            inc_bracket3: float
            inc_bracket4: float
            total_households: int
            household_pop: float
            avg_size: float
            total_employment: float
    }

}

#### TAZ.json

Ibid, but less properties. Only N___CO_TAZ and AREA

## Aggregated

#### allRoutes.json

List of all routes information, pulled from BusRoutes_UTA

STRUCTURE:
Array of route objects: {
    lineAbbr: string
    lineName: string
    service: string
    shape_length: float
    busses: array of bus IDs (strings)
    coordinates: array of coordinate pairs (floats) (shape: Lx2x2)
        *i.e. [
            [[-111.85115002947421, 40.76702999260385], [-111.85160002925915, 40.767020006406966]],
            [[-111.85160002925915, 40.767020006406966], [-111.8520399943318, 40.7670500000036]]
            ...
        ]*
    path_length: float
}

#### allStops.json

Array of all bus stops and assoc info drawn from BusStops_UTA.json

STRUCTURE:
Array of stop objects: {
    stopId: int
    stopName: string
    streetNum: int
    onStreet: tring
    atStreet: string
    city: sting
    inService: bool
    bench: bool
    shelter: bool
    lighting: bool
    locationUs: string
    UTAStopID: string
    coordinates: array of coordinates (size 2, floats)
}

#### BusesAtStations.json

Pre-populated obect for tracking bus locations over the course of the day

STRUCTURE:
object {
    STOP_NAME : {
        stop_id: int
        stop_name: string
        busTimes: object of time keys {
            "0:00" : array of bus ID's
            "1.00" : array of bus ID's
            etc
        }
    }
}
