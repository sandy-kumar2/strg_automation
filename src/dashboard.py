import matplotlib.pyplot as plt


def create_dashboard(
    techno_capacity,
    system_capacity,
    techno_luns,
    system_luns
):

    plt.figure(figsize=(10, 5))

    labels = [
        "Techno Report",
        "System Export"
    ]

    capacities = [
        techno_capacity,
        system_capacity
    ]

    plt.bar(
        labels,
        capacities
    )

    plt.title(
        "Storage Capacity Comparison (TiB)"
    )

    plt.ylabel("TiB")

    plt.tight_layout()

    plt.show()