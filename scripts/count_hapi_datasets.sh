#!/bin/sh

#
# Usage:
#   ./count_hapi_datasets.sh [URL-to-HAPI-server-list]
#
# If no URL is provided, use the default HAPI server list.
#
# Requires:
#   curl
#   jq
#

DEFAULT_SERVER_LIST_URL="https://raw.githubusercontent.com/hapi-server/servers/refs/heads/master/abouts.json"

if [ "$#" -gt 1 ]; then
    echo "Usage: $0 [URL-to-HAPI-server-list]"
    exit 1
fi

SERVER_LIST_URL="${1:-$DEFAULT_SERVER_LIST_URL}"

# Fetch the server list once.
server_list_json=$(curl -LfsS "$SERVER_LIST_URL")

if [ "$?" -ne 0 ]; then
    echo "ERROR: Could not retrieve HAPI server list:"
    echo "       $SERVER_LIST_URL"
    exit 1
fi

# Determine the width needed for the server ID column.
# Use at least 12 characters, but expand if any ID is longer.
id_width=$(
    printf '%s\n' "$server_list_json" |
    jq '[.[].id | length] | max // 0'
)

if [ "$id_width" -lt 12 ]; then
    id_width=12
fi

# Extract ID and URL together as tab-separated values.
server_rows=$(
    printf '%s\n' "$server_list_json" |
    jq -r '.[] |
           select(.id != null and .x_url != null) |
           [.id, .x_url] | @tsv'
)

total_servers=0
total_datasets=0

# Store a tab character for use as the read delimiter.
TAB=$(printf '\t')

# Use a here-document rather than a pipeline so that changes to
# total_servers and total_datasets remain visible after the loop.
while IFS="$TAB" read -r server_id server_url
do
    total_servers=$((total_servers + 1))

    # Remove a trailing slash, if present.
    server_url=${server_url%/}

    catalog_url="${server_url}/catalog"

    count=$(
        curl -LfsS "$catalog_url" 2>/dev/null |
        jq -r '.catalog | length' 2>/dev/null
    )

    if [ -n "$count" ]; then
        total_datasets=$((total_datasets + count))

        printf "%6s  %-*s  %s\n" \
            "$count" "$id_width" "$server_id" "$server_url"
    else
        printf "%6s  %-*s  %s\n" \
            "ERROR" "$id_width" "$server_id" "$server_url"
    fi

done <<EOF
$server_rows
EOF

echo
echo "Total HAPI servers:  $total_servers"
echo "Total HAPI datasets: $total_datasets"

