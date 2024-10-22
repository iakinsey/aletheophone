export type UseDataResponse<T> = {
    data: T | undefined;
    error: Error | undefined;
    loading: boolean;
};