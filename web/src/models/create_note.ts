export default class CreateNote {
    text: string

    constructor(text: string) {
        this.text = text;
    }

    toCreateRequest(): [string, RequestInit] {
        const params: RequestInit = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: this.text
            })
        }

        return ["/note", params]
    }
}