export interface ExamineeAPI {
    id: string;
    first_name: string;
    last_name: string;
    internal_identifier: string;
    created_at: string;
    updated_at?: string; // Optional, if applicable
}

export interface ExamineeAPIRequest {
    first_name: string;
    last_name: string;
    internal_identifier: string;
}