# This file allows building and running the software with the Nix package
# manager, used in NixOS or on another distribution.

{
  description = "crunch is a lossy image compression format meant for video games — daemon engine's fork";

  inputs = {
    nixpkgs.url = "flake:nixpkgs";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {

      defaultPackage.x86_64-linux =
        pkgs.stdenv.mkDerivation {
          name = "crunch";
          src = pkgs.lib.cleanSource ./.;
          buildInputs = with pkgs; [
            gcc cmake
          ];
        };

      defaultApp.x86_64-linux = {
        type = "app";
        program = "${self.defaultPackage.x86_64-linux}/bin/crunch";
      };

    };
}
