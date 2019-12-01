import asyncio
import iterm2


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='kubectl context',
        detailed_description='The currently configured Kubernetes context for kubectl',
        exemplar='⎈ docker-for-desktop',
        update_cadence=2,
        identifier='engineering.dane.iterm-components.kubectl-context',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def kubectl_context_coroutine(knobs):
        ctx_proc = await asyncio.create_subprocess_shell(
            'kubectl config current-context',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        ns_proc = await asyncio.create_subprocess_shell(
            'kubectl config view --minify --output "jsonpath={..namespace}"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        ctx_stdout, ctx_stderr = await ctx_proc.communicate()
        ns_stdout, ns_stderr = await ns_proc.communicate()
        return f'⎈ {ctx_stdout.decode().strip()}|{ns_stdout.decode().strip()}' if not ctx_stderr else '⎈ kubectl not installed!'

    await component.async_register(connection, kubectl_context_coroutine)

iterm2.run_forever(main)
