import reflex as rx

config = rx.Config(
    app_name="wordle_clone",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)