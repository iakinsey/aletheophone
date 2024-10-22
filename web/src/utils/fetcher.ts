import useSWR from "swr";
import { UseDataResponse } from "../models/rpc";

const BASE_URL = "http://localhost:8000"

const fetcher = async (url: string, body: RequestInit) => {
    const resp = await fetch(url, body);

    if (!resp.ok) {
        throw new Error(`${resp.status} ${resp.url}`)
    }

    return resp.json();
} 

export const useData = <T>(u: string, body: RequestInit): UseDataResponse<T> => {
    let url = BASE_URL + u;
    const { data, error } = useSWR([url, body], ([url, body]) => fetcher(url, body));

    return {
        data,
        error,
        loading: !error && ! data
    }
}

export const fetchRpc = async <T>(url: string, body: RequestInit): Promise<T> => {
      const resp = await fetch(BASE_URL + url, body);

      if (!resp.ok) {
        throw new Error(`${resp.status} ${resp.url}`);
      }

      const data: T = await resp.json();

      return data;
}