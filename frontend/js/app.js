// State Management
const SearchState = {
    query: {
        product: "",
        indian_company: "",
        foreign_company: ""
    },
    results: null,
    loading: false,
    fields: {
        // existing fields
    },
    error: null,
    pagination: {
        currentPage: 1,
        hasMore: true
    }
}

const ColumnState = {
    settingsOpen: false,
    groups: {
        transaction: {
            label: "1. Transaction Details",
            columns: {
                BillNO: true,
                Date: true,
                Invoice_No: true,
                Item_No: true
            }
        },
        product: {
            label: "2. Product Information",
            columns: {
                "4Digit": true,
                HSCode: true,
                Product: true,
                Quantity: true,
                Unit: true,
                Item_Rate_INV: true,
                Item_Rate_INR: true
            }
        },
        pricing: {
            label: "3. Pricing & Currency",
            columns: {
                Currency: true,
                Total_Amount_INV_FC: true,
                FOB_INR: true
            }
        },
        trade: {
            label: "4. Trade Parties",
            columns: {
                IndianCompany: true,
                ForeignCompany: true,
                IEC: true,
                IEC_PIN: true,
                CUSH: true
            }
        },
        location: {
            label: "5. Location Details",
            columns: {
                ForeignPort: true,
                ForeignCountry: true,
                IndianPort: true,
                Address1: true,
                Address2: true,
                City: true
            }
        }
    },
    collapsed: {
        transaction: false,
        product: false,
        pricing: false,
        trade: false,
        location: false
    }
}

// Add Info Component
const InfoSection = {
    view: function() {
        return m("div.info-section", [
            m("h2", "Indian Export Data Search"),
            m("p", "This tool helps you search through Indian export data from June 2016."),
            m("div.search-tips", [
                m("h3", "How to use:"),
                m("ul", [
                    m("li", "Search products by entering keywords (e.g., 'cotton', 'steel')"),
                    m("li", "Find specific Indian companies by name"),
                    m("li", "Look up foreign companies importing from India"),
                    m("li", "Combine any of these fields for more specific results")
                ]),
                m("p.tip", "💡 Tip: Searches are case-insensitive and partial matches are supported")
            ])
        ])
    }
}

// Add SearchForm Component
const SearchForm = {
    view: function() {
        const selectedColumnCount = ColumnToggles.getSelectedCount();
        const hasValue = SearchState.query.product?.trim() || 
                        SearchState.query.indian_company?.trim() || 
                        SearchState.query.foreign_company?.trim();

        return m("form.search-form", {
            onsubmit: (e) => {
                e.preventDefault();
                
                if (!hasValue) {
                    SearchState.error = "Please fill out at least one search field before searching";
                    return;
                }

                if (selectedColumnCount === 0) {
                    return; // Just return without showing warning
                }
                
                // Reset pagination state for new search
                SearchState.pagination = {
                    currentPage: 1,
                    hasMore: true
                };
                
                SearchState.loading = true;
                SearchState.error = null;  // Clear any previous errors
                
                m.request({
                    method: "GET",
                    url: "http://localhost:8000/search",
                    params: {
                        ...SearchState.query,
                        page: 1  // Reset to first page
                    }
                })
                .then(function(result) {
                    SearchState.results = result;
                    SearchState.loading = false;
                })
            }
        }, [
            // Search Fields
            m("div.search-fields", [
                // Product field
                m("div.field", [
                    m("label", "Product"),
                    m("input[type=text]", {
                        placeholder: "e.g., cotton, steel",
                        value: SearchState.query.product,
                        onchange: function(e) { 
                            SearchState.query.product = e.target.value 
                        }
                    })
                ]),
                // Indian Company field
                m("div.field", [
                    m("label", "Indian Company"),
                    m("input[type=text]", {
                        placeholder: "Enter company name",
                        value: SearchState.query.indian_company,
                        onchange: function(e) { 
                            SearchState.query.indian_company = e.target.value 
                        }
                    })
                ]),
                // Foreign Company field
                m("div.field", [
                    m("label", "Foreign Company"),
                    m("input[type=text]", {
                        placeholder: "Enter foreign company name",
                        value: SearchState.query.foreign_company,
                        onchange: function(e) { 
                            SearchState.query.foreign_company = e.target.value 
                        }
                    })
                ])
            ]),
            
            // Error message
            SearchState.error && m("div.error-message", SearchState.error),
            
            // Column Selection (between fields and button)
            m("div.column-selection", [
                m(ColumnToggles)
            ]),
            
            // Button container for search and clear
            m("div.button-group", [
                m("button[type=submit]", {
                    class: "search-btn"
                }, "Search"),
                
                m("button[type=button]", {
                    class: "clear-btn",
                    onclick: (e) => {
                        e.preventDefault();
                        // Clear all search fields
                        SearchState.query = {
                            product: "",
                            indian_company: "",
                            foreign_company: ""
                        };
                        // Clear results if any
                        SearchState.results = null;
                        SearchState.error = null;
                    }
                }, "Clear Filters")
            ])
        ])
    }
}

// Update the date formatting in TableView
const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`;
};

// Add this new component after SearchForm
const TableView = {
    getSelectedColumns() {
        // Get all selected columns from ColumnState
        const selected = [];
        Object.values(ColumnState.groups).forEach(group => {
            Object.entries(group.columns).forEach(([colName, isVisible]) => {
                if (isVisible) selected.push(colName);
            });
        });
        return selected;
    },

    oncreate: function(vnode) {
        window.addEventListener('scroll', () => {
            if (this.shouldLoadMore()) {
                this.loadMore();
            }
        });
    },

    shouldLoadMore() {
        if (!SearchState.results || !SearchState.pagination.hasMore || SearchState.loading) {
            return false;
        }

        const table = document.querySelector('.table-container');
        if (!table) return false;

        const bottomOfTable = table.getBoundingClientRect().bottom;
        const bottomOfWindow = window.innerHeight;

        return bottomOfTable <= bottomOfWindow + 100;
    },

    loadMore() {
        if (SearchState.loading) return;
        
        SearchState.loading = true;
        SearchState.pagination.currentPage++;

        console.log("Loading page:", SearchState.pagination.currentPage); // Debug

        m.request({
            method: "GET",
            url: "http://localhost:8000/search",
            params: {
                ...SearchState.query,
                page: SearchState.pagination.currentPage
            }
        })
        .then(function(result) {
            console.log("New results:", result); // Debug

            if (result.results && result.results.length > 0) {
                // Combine old and new results
                const currentResults = SearchState.results.results || [];
                SearchState.results.results = [
                    ...currentResults,
                    ...result.results
                ];
                
                // Update pagination state
                SearchState.pagination.hasMore = result.has_more;
                SearchState.results.total_matches = result.total_matches;
            } else {
                SearchState.pagination.hasMore = false;
            }
            
            SearchState.loading = false;
            m.redraw(); // Force Mithril to update the view
        })
        .catch(function(error) {
            console.error("Error loading more results:", error);
            SearchState.loading = false;
            SearchState.error = "Failed to load more results";
            m.redraw();
        });
    },

    view: function() {
        if (SearchState.loading && !SearchState.results) {
            return m("div.loading", "Loading...")
        }

        if (!SearchState.results) {
            return null;
        }

        const selectedColumns = this.getSelectedColumns();

        return [
            // Results summary
            m("div.results-summary", [
                m("p", [
                    `Found ${SearchState.results.total_matches} results `,
                    m("span.showing-count", 
                        `(Showing ${SearchState.results.results.length} rows)`
                    )
                ])
            ]),
            
            // Updated table with row numbers
            m("div.table-container", [
                m("table", [
                    m("thead", 
                        m("tr", [
                            m("th.row-number", "#"),  // Add number column header
                            selectedColumns.map(colName => 
                                m("th", colName)
                            )
                        ])
                    ),
                    m("tbody", 
                        SearchState.results.results.map((row, index) => 
                            m("tr", [
                                m("td.row-number", index + 1),  // Add row number
                                selectedColumns.map(colName => 
                                    m("td", colName === 'Date' ? 
                                        formatDate(row[colName]) : 
                                        row[colName]
                                    )
                                )
                            ])
                        )
                    )
                ])
            ]),
            
            // Loading indicator for more results
            SearchState.loading && m("div.loading-more", "Loading more results...")
        ];
    }
}

// Update ColumnToggles Component
const ColumnToggles = {
    getSelectedCount() {
        let count = 0;
        Object.values(ColumnState.groups).forEach(group => {
            Object.values(group.columns).forEach(isVisible => {
                if (isVisible) count++;
            });
        });
        return count;
    },
    
    view: function() {
        return m("div.settings-dropdown", [
            // Settings Toggle Button
            m("button.settings-toggle", {
                onclick: (e) => {
                    ColumnState.settingsOpen = !ColumnState.settingsOpen;
                },
                // Prevent Enter key from triggering the toggle
                onkeydown: (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                    }
                },
                type: "button"  // Explicitly set button type to prevent form submission
            }, [
                m("span.gear-icon", "⚙️"),
                "Selected columns"
            ]),
            
            // Settings content
            ColumnState.settingsOpen && m("div.settings-content", [
                // Toggle all columns switch
                m("div.toggle-all", [
                    m("label.toggle-switch", [
                        m("input[type=checkbox]", {
                            checked: ColumnToggles.areAllColumnsSelected(),
                            onclick: (e) => {
                                const selectAll = e.target.checked;
                                Object.keys(ColumnState.groups).forEach(groupKey => {
                                    Object.keys(ColumnState.groups[groupKey].columns).forEach(colName => {
                                        ColumnState.groups[groupKey].columns[colName] = selectAll;
                                    });
                                });
                            }
                        }),
                        m("span.slider"),
                        m("span.toggle-label", "Show All Columns")
                    ])
                ]),
                
                // Existing column groups
                Object.entries(ColumnState.groups).map(([key, group]) =>
                    m("div.column-group", [
                        m("div.group-header", {
                            onclick: () => {
                                ColumnState.collapsed[key] = !ColumnState.collapsed[key];
                            }
                        }, [
                            m("span.arrow", ColumnState.collapsed[key] ? "▶" : "▼"),
                            m("span.label", group.label)
                        ]),
                        !ColumnState.collapsed[key] && m("div.column-list", 
                            Object.entries(group.columns).map(([columnName, isVisible]) =>
                                m("div.column-item", {
                                    class: isVisible ? 'selected' : '',
                                    onclick: () => {
                                        group.columns[columnName] = !isVisible;
                                    }
                                }, columnName)
                            )
                        )
                    ])
                )
            ])
        ])
    },

    // Helper method to check if all columns are selected
    areAllColumnsSelected: () => {
        return Object.values(ColumnState.groups).every(group => 
            Object.values(group.columns).every(isVisible => isVisible)
        );
    }
}


const App = {
    view: function() {
        return m("div.container", [
            m("h1", "Export Search"),
            m(InfoSection),  // Add the info section
            m(SearchForm),
            m(TableView)
        ])
    }
}

// Initialize the app
m.mount(document.getElementById("app"), App)