# Stage de build
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build

WORKDIR /source

COPY DotNet.Docker.csproj ./

RUN dotnet restore 

COPY . ./

RUN dotnet publish -o build -c Release
# /source/build/DotNet.Docker.dll

# Stage de publication
FROM mcr.microsoft.com/dotnet/aspnet:7.0

WORKDIR /app

COPY --from=build /source/build .

ENTRYPOINT [ "dotnet", "DotNet.Docker.dll" ]