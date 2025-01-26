export const toCamelCase = (str: string): string => {
    return str.replace(/([-_][a-z])/g, (group) =>
        group.toUpperCase().replace('-', '').replace('_', ''),
    );
};

export const toSnakeCase = (str: string): string => {
    return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
};

export const transformKeys = <T extends object>(
    obj: T,
    transform: (key: string) => string,
): unknown => {
    if (Array.isArray(obj)) {
        return obj.map((v) => transformKeys(v, transform));
    } else if (obj !== null && obj.constructor === Object) {
        return Object.fromEntries(
            Object.entries(obj).map(([key, value]) => [
                transform(key),
                value && typeof value === 'object'
                    ? transformKeys(value, transform)
                    : value,
            ]),
        );
    }
    return obj;
};
