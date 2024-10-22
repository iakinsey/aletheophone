export default class GetNote {
    id: number

    constructor(id: number) {
        this.id = id;
    }

    toGetRequest(): [string, RequestInit] {
        return [
            "/note/" + this.id,
            {method: 'GET'}
        ]
    }
}
