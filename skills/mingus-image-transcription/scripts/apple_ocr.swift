import AppKit
import Foundation
import Vision

guard CommandLine.arguments.count >= 2 else {
    fputs("usage: swift apple_ocr.swift /path/to/image\n", stderr)
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let imageUrl = URL(fileURLWithPath: imagePath)

guard let image = NSImage(contentsOf: imageUrl) else {
    fputs("failed to load image\n", stderr)
    exit(1)
}

guard let tiff = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let cgImage = bitmap.cgImage else {
    fputs("failed to convert image\n", stderr)
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLanguages = ["zh-Hans", "en-US"]
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

do {
    try handler.perform([request])
    let observations = request.results ?? []
    let lines = observations.compactMap { $0.topCandidates(1).first?.string.trimmingCharacters(in: .whitespacesAndNewlines) }
        .filter { !$0.isEmpty }
    print(lines.joined(separator: "\n"))
} catch {
    fputs("ocr failed: \(error)\n", stderr)
    exit(1)
}
