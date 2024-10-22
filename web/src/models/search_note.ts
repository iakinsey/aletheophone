export default class SearchNote {
  limit: number;
  offset: number;

  constructor(
    limit: number = 25,
    offset: number = 0,
  ) {
    this.limit = limit;
    this.offset = offset;
  }

  static fromUrlQuery(query: string): SearchNote {
    const params = new URLSearchParams(query);
    const limit = parseInt(params.get('limit') || '10', 10);
    const offset = parseInt(params.get('offset') || '0', 10);

    return new SearchNote(limit, offset);
  }

  toQueryUrl(): string {
    const params = new URLSearchParams();
    if (this.limit) params.set('limit', this.limit.toString());
    if (this.offset) params.set('offset', this.offset.toString());

    return "/search?" + params.toString();
  }
  
  toGetNotesRequest(): [string, RequestInit] {
    const params: RequestInit = {
      method: 'GET',
    }

    const obj = Object.fromEntries(
      Object.entries(this).map(([key, value]) => [key, String(value)])
    );
  
    const searchParams = new URLSearchParams(obj);
    const url = "/notes?" + searchParams;

    return [url, params]
  }
}