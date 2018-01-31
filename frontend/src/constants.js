export const WEEK = 604800
export const YEAR = 31536000

export const SORT_BY = [
  {
    value: 'best-selling',
    label: 'Popularity'
  },
  {
    value: 'discount_price',
    label: 'Price: Low to High'
  },
  {
    value: '-discount_price',
    label: 'Price: High to Low'
  },
  {
    value: 'name',
    label: 'A-Z'
  },
  {
    value: '-name',
    label: 'Z-A'
  },
  {
    value: 'created_at',
    label: 'Newest to Oldest'
  },
  {
    value: '-created_at',
    label: 'Oldest to Newest'
  },
]

export const DEFAULT_SORT_BY = '-created_at'
